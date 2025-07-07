import { Component, OnInit } from '@angular/core';
import { Product } from 'src/app/shared/models/product';
import { ShopService } from '../shop.service';
import { ActivatedRoute } from '@angular/router';
import { BreadcrumbService } from 'xng-breadcrumb';
import { BasketService } from 'src/app/basket/basket.service';
import { take } from 'rxjs';
import { trace } from '@opentelemetry/api';

@Component({
  selector: 'app-product-details',
  templateUrl: './product-details.component.html',
  styleUrls: ['./product-details.component.scss']
})
export class ProductDetailsComponent implements OnInit {
  product?: Product;
  quantity = 1;
  quantityInBasket = 0;
  private tracer = trace.getTracer('angular-app');

  constructor(private shopService: ShopService, private activatedRoute: ActivatedRoute, 
    private bcService: BreadcrumbService, private basketService: BasketService) {
      this.bcService.set('@productDetails', ' ')
    }

  ngOnInit(): void {
    this.loadProduct();
  }

  loadProduct() {
    const span = this.tracer.startSpan('loadProduct');
    span.addEvent('Loading product details');
    const id = this.activatedRoute.snapshot.paramMap.get('id');
    if (id) this.shopService.getProduct(+id).subscribe({
      next: product => {
        this.product = product;
        span.setAttribute('productId', product.name);
        span.setAttribute('productType', product.productType);
        span.setAttribute('productType', product.productBrand);
        this.bcService.set('@productDetails', product.name);
        this.basketService.basketSource$.pipe(take(1)).subscribe({
          next: basket => {
            const item = basket?.items.find(x => x.id === +id);
            if (item) {
              this.quantity = item.quantity;
              this.quantityInBasket = item.quantity;
            }
          }
        })
      },
      error: error => console.log(error)
    })
    span.end();
  }

  incrementQuantity() {
    this.quantity++;
  }

  decrementQuantity() {
    this.quantity--;
  }

  updateBasket() {
    const span = this.tracer.startSpan('updateBasket');
    
    if (this.product) {
      span.addEvent('Updating basket with product');
      span.setAttribute('productName', this.product.name);
      span.setAttribute('productQuantity', this.quantity);
      if (this.quantity > this.quantityInBasket) {
        const itemsToAdd = this.quantity - this.quantityInBasket;
        this.quantityInBasket += itemsToAdd;
        this.basketService.addItemToBasket(this.product, itemsToAdd);
      } else {
        const itemsToRemove = this.quantityInBasket - this.quantity;
        this.quantityInBasket -= itemsToRemove;
        this.basketService.removeItemFromBasket(this.product.id, itemsToRemove);
      }
    }
    span.end();
  }

  get buttonText() {
    return this.quantityInBasket === 0 ? 'Add to basket' : 'Update basket';
  }
}
