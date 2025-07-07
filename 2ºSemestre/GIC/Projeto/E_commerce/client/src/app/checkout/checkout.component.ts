import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, AbstractControl, ValidationErrors, ValidatorFn} from '@angular/forms';
import { AccountService } from '../account/account.service';
import { BasketService } from '../basket/basket.service';

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.scss']
})
export class CheckoutComponent implements OnInit {

  constructor(private fb: FormBuilder, private accountService: AccountService, private basketService: BasketService) { }

  ngOnInit(): void {
    this.getAddressFormValues();
    this.getDeliveryMethodValue();
  }
  
  checkoutForm = this.fb.group({
    addressForm: this.fb.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      street: ['', Validators.required],
      city: ['', Validators.required],
      state: ['', Validators.required],
      zipcode: ['', Validators.required],
    }),
    deliveryForm: this.fb.group({
      deliveryMethod: ['', Validators.required]
    }),
    paymentForm: this.fb.group({
      nameOnCard: ['', Validators.required],
      cardNumber: ['', [Validators.required, luhnValidator]],
      cardExpiry: ['', [Validators.required, expiryValidator]],
      cardCvc: ['', [Validators.required, Validators.pattern(/^\d{3,4}$/)]],
    })
  });

  getAddressFormValues() {
    this.accountService.getUserAddress().subscribe({
      next: address => {
        address && this.checkoutForm.get('addressForm')?.patchValue(address)
      }
    })
  }

  getDeliveryMethodValue() {
    const basket = this.basketService.getCurrentBasketValue();
    if (basket && basket.deliveryMethodId) {
      this.checkoutForm.get('deliveryForm')?.get('deliveryMethod')
        ?.patchValue(basket.deliveryMethodId.toString());
    }
  }

}

export const luhnValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const value = control.value?.replace(/\D/g, '');
  if (!/^\d{16}$/.test(value)) return { invalidCardNumber: true };

  let sum = 0;
  let alternate = false;
  for (let i = value.length - 1; i >= 0; i--) {
    let n = parseInt(value[i], 10);
    if (alternate) {
      n *= 2;
      if (n > 9) n -= 9;
    }
    sum += n;
    alternate = !alternate;
  }

  return (sum % 10 === 0) ? null : { invalidCardNumber: true };
};

export const expiryValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const value = control.value;
  if (!/^\d{2}\/\d{2}$/.test(value)) return { invalidExpiry: true };

  const [month, year] = value.split('/').map(Number);
  if (month < 1 || month > 12) return { invalidExpiry: true };

  const currentYear = new Date().getFullYear() % 100;
  const currentMonth = new Date().getMonth() + 1;
  if (year < currentYear || (year === currentYear && month < currentMonth)) {
    return { invalidExpiry: true };
  }

  return null;
};