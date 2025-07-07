import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { BasketService } from 'src/app/basket/basket.service';
import { Basket } from 'src/app/shared/models/basket';
import { Address } from 'src/app/shared/models/user';
import { CheckoutService } from '../checkout.service';
import { NavigationExtras, Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';
import { OrderToCreate } from 'src/app/shared/models/order';

@Component({
  selector: 'app-checkout-payment',
  templateUrl: './checkout-payment.component.html',
  styleUrls: ['./checkout-payment.component.scss'],
})
export class CheckoutPaymentComponent {
  @Input() checkoutForm?: FormGroup;
  loading = false;

  constructor(
    private basketService: BasketService,
    private checkoutService: CheckoutService,
    private toastr: ToastrService,
    private router: Router
  ) {}
  
  get paymentFormComplete() {
    return this.checkoutForm?.get('paymentForm')?.valid;
  }

  async submitOrder() {
    this.loading = true;
    const basket = this.basketService.getCurrentBasketValue();
    if (!basket) throw new Error('Cannot get basket');

    try {
      const createdOrder = await this.createOrder(basket);
      this.basketService.deleteBasket(basket);
      const navigationExtras: NavigationExtras = { state: createdOrder };
      this.router.navigate(['checkout/success'], navigationExtras);
    } catch (error: any) {
      console.log(error);
      this.toastr.error(error.message);
    } finally {
      this.loading = false;
    }
  }

  private async createOrder(basket: Basket | null) {
    if (!basket) throw new Error('Basket is null');
    const orderToCreate = this.getOrderToCreate(basket);
    return firstValueFrom(this.checkoutService.createOrder(orderToCreate));
  }

  private getOrderToCreate(basket: Basket): OrderToCreate {
    const deliveryMethodId = this.checkoutForm?.get('deliveryForm')?.get('deliveryMethod')?.value;
    const shipToAddress = this.checkoutForm?.get('addressForm')?.value as Address;
    if (!deliveryMethodId || !shipToAddress) throw new Error('Problem with basket');
    return {
      basketId: basket.id,
      deliveryMethodId: deliveryMethodId,
      shipToAddress: shipToAddress
    };
  }
}
