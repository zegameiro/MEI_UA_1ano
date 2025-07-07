import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Order } from '../shared/models/order';
import { trace } from '@opentelemetry/api';

@Injectable({
  providedIn: 'root'
})
export class OrdersService {

  // 3. add 2 methods in the order service to get the list of orders and a single order

  baseUrl = environment.apiUrl;
  private tracer = trace.getTracer('angular-app');

  constructor(private http: HttpClient) { }

  getOrdersForUser() {
    const span = this.tracer.startSpan('getOrdersForUser');
    span.addEvent('Fetching orders for user');
    span.end();
    return this.http.get<Order[]>(this.baseUrl + 'orders');
  }
  getOrderDetailed(id: number) {
    const span = this.tracer.startSpan('getOrderDetailed');
    span.addEvent('Fetching order details');
    span.end();
    return this.http.get<Order>(this.baseUrl + 'orders/' + id);
  }
}
