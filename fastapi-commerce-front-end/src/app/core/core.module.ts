import { Provider } from '@angular/core';
import { CategoryService } from '../admin/admin-categories/categories.service';
import { ProductService } from '../admin/admin-products/products.service';

export function provideCore(): Provider[] {
  return [
    { provide: CategoryService },
    { provide: ProductService }
  ];
}
