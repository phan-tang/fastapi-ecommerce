import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';

import { ProductData, ProductListData } from '../../shared/interfaces/product.interfaces';

@Injectable()
export class ProductService {
  resource: string = 'products';

  constructor(private http: HttpClient) { }

  getProducts(params: string): Observable<ProductListData> {
    return this.http.get<ProductListData>(environment.apiURL + this.resource + params);
  }

  getProductById(id: string): Observable<ProductData> {
    return this.http.get<ProductData>(environment.apiURL + this.resource + `/${id}`);
  }
}
