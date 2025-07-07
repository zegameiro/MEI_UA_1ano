import { Component } from '@angular/core';
import { AbstractControl, AsyncValidatorFn, FormBuilder, Validators } from '@angular/forms';
import { AccountService } from '../account.service';
import { Router } from '@angular/router';
import { debounceTime, finalize, map, switchMap, take } from 'rxjs';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  errors: string[] | null = null;

  constructor(private fb: FormBuilder, private accountService: AccountService, private router: Router) {}

  complexPassword = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+}{":;'?/>,.<])(?!.*\s).{6,10}$/;
  
  registerForm = this.fb.group({
    displayName: ['', Validators.required],
    email: ['', [Validators.required, Validators.email], [this.validateEmailNotTaken()]],
    password: ['', [Validators.required, Validators.pattern(this.complexPassword)]],
  })  

  get password() {
    return this.registerForm.get('password')!;
  }
  
  passwordRequirements = [
    { label: 'At least one digit', test: (v: string) => /\d/.test(v) },
    { label: 'One lowercase letter', test: (v: string) => /[a-z]/.test(v) },
    { label: 'One uppercase letter', test: (v: string) => /[A-Z]/.test(v) },
    { label: 'One special character', test: (v: string) => /[!@#$%^&*()_+}{":;'?/>,.<]/.test(v) },
    { label: 'No spaces', test: (v: string) => /^\S+$/.test(v) },
    { label: '6 to 10 characters', test: (v: string) => /^.{6,10}$/.test(v) }
  ];
  
  onSubmit() {
    this.accountService.register(this.registerForm.value).subscribe({
      next: () => this.router.navigateByUrl('/shop'),
      error: error => this.errors = error.errors
    })
  }

  validateEmailNotTaken(): AsyncValidatorFn {
    return (control: AbstractControl) => {
      return control.valueChanges.pipe(
        debounceTime(1000),
        take(1),
        switchMap(() => {
          return this.accountService.checkEmailExists(control.value).pipe(
            map(result => result ? {emailExists: true} : null),
            finalize(() => control.markAsTouched())
          )
        })
      )
    }
  }
}
