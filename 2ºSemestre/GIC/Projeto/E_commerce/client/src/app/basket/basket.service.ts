import { Injectable } from '@angular/core';
import { BehaviorSubject, map } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Basket, BasketItem, BasketTotals } from '../shared/models/basket';
import { HttpClient } from '@angular/common/http';
import { Product } from '../shared/models/product';
import { DeliveryMethod } from '../shared/models/deliveryMethod';
import { trace } from '@opentelemetry/api';

@Injectable({
  providedIn: 'root'
})
export class BasketService {
  baseUrl = environment.apiUrl;
  private basketSource = new BehaviorSubject<Basket | null>(null);
  basketSource$ = this.basketSource.asObservable();
  private basketTotalSource = new BehaviorSubject<BasketTotals | null>(null);
  basketTotalSource$ = this.basketTotalSource.asObservable();

  private tracer = trace.getTracer('angular-app');

  constructor(private http: HttpClient) { }

  createPaymentIntent() {
    return this.http.post<Basket>(this.baseUrl + 'payments/' + this.getCurrentBasketValue()?.id, {})
      .pipe(
        map(basket => {
          this.basketSource.next(basket);
        })
      )
  }

  setShippingPrice(deliveryMethod: DeliveryMethod) {
    const basket = this.getCurrentBasketValue();
    if (basket) {
      basket.shippingPrice = deliveryMethod.price;
      basket.deliveryMethodId = deliveryMethod.id;
      this.setBasket(basket);
    }
  }

  getBasket(id: string) {
    const span = this.tracer.startSpan('getBasket');
    span.setAttribute('basketId', id);
    span.addEvent('Fetching basket from server');
    span.end();
    return this.http.get<Basket>(this.baseUrl + 'basket?id=' + id).subscribe({
      next: basket => {
        this.basketSource.next(basket);
        this.calculateTotals();
      }
    })
  }

  setBasket(basket: Basket) {
    const span = this.tracer.startSpan('setBasket');
    span.setAttribute('basketId', basket.id);
    span.addEvent('Setting basket on server');
    span.end();
    return this.http.post<Basket>(this.baseUrl + 'basket', basket).subscribe({
      next: basket => {
        this.basketSource.next(basket);
        this.calculateTotals();
      }
    })
  }

  getCurrentBasketValue() {
    return this.basketSource.value;
  }

  addItemToBasket(item: Product | BasketItem, quantity = 1) {
    const span = this.tracer.startSpan('addItemToBasket');
    if (this.isProduct(item)) item = this.mapProductItemToBasketItem(item);
    const basket = this.getCurrentBasketValue() ?? this.createBasket();
    basket.items = this.addOrUpdateItem(basket.items, item, quantity);
    this.setBasket(basket);
    span.setAttribute('itemName', item.productName);
    span.setAttribute('itemQuantity', item.quantity);
    span.setAttribute('itemPrice', item.price);
    span.addEvent('Item added to basket');
    span.end();
  }

  removeItemFromBasket(id: number, quantity = 1) {
    const span = this.tracer.startSpan('removeItemFromBasket');
    const basket = this.getCurrentBasketValue();
    if (!basket) return;
    const item = basket.items.find(x => x.id === id);
    span.setAttribute('itemName', item?.productName ?? 'Unknown');
    span.setAttribute('itemQuantity', quantity);
    if (item) {
      item.quantity -= quantity;
      if (item.quantity === 0) {
        basket.items = basket.items.filter(x => x.id !== id);
      }
      if (basket.items.length > 0) this.setBasket(basket);
      else this.deleteBasket(basket);
    }
    span.addEvent('Item removed from basket');
    span.end();
  }

  deleteBasket(basket: Basket) {
    const span = this.tracer.startSpan('deleteBasket');
    span.setAttribute('basketId', basket.id);
    span.addEvent('Deleting basket from server');
    span.end();
    return this.http.delete(this.baseUrl + 'basket?id=' + basket.id).subscribe({
      next: () => {
        this.deleteLocalBasket();
      }
    })
  }

  deleteLocalBasket() {
    this.basketSource.next(null);
    this.basketTotalSource.next(null);
    localStorage.removeItem('basket_id');
  }
  
  private addOrUpdateItem(items: BasketItem[], itemToAdd: BasketItem, quantity: number): BasketItem[] {
    const span = this.tracer.startSpan('addOrUpdateItem');
    span.setAttribute('itemName', itemToAdd.productName);
    span.setAttribute('itemQuantity', quantity);
    span.setAttribute('itemPrice', itemToAdd.price);
    span.addEvent('Adding or updating item in basket');

    const item = items.find(x => x.id === itemToAdd.id);
    if (item) item.quantity += quantity;
    else {
      itemToAdd.quantity = quantity;
      items.push(itemToAdd);
    }
    span.end();
    return items;
  }

  private createBasket(): Basket {
    const basket = new Basket();
    localStorage.setItem('basket_id', basket.id);
    return basket;
  }

  private mapProductItemToBasketItem(item: Product): BasketItem {
    return {
      id: item.id,
      productName: item.name,
      price: item.price,
      quantity: 0,
      pictureUrl: item.pictureUrl,
      brand: item.productBrand,
      type: item.productType
    }
  }

  private calculateTotals() {
    const basket = this.getCurrentBasketValue();
    if (!basket) return;
    const subtotal = basket.items.reduce((a, b) => (b.price * b.quantity) + a, 0);
    const total = subtotal + basket.shippingPrice;
    this.basketTotalSource.next({shipping: basket.shippingPrice, total, subtotal});
  }

  private isProduct(item: Product | BasketItem): item is Product {
    return (item as Product).productBrand !== undefined;
  }
}
