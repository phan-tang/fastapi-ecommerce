import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';
import { CategoryData } from '../../shared/interfaces/category.interfaces';

@Injectable()
export class CategoryService {
  resource: string = 'categories';

  constructor(private http: HttpClient) { }

  getCategories(params: string): Observable<CategoryData[]> {
    return this.http.get<CategoryData[]>(environment.apiURL + this.resource);
  }
}
