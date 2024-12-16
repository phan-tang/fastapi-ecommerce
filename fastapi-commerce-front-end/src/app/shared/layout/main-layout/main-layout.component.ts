import { Component, inject } from '@angular/core';
import { FooterComponent } from '../footer/footer.component';
import { HeaderComponent } from '../header/header.component';
import { RouterOutlet } from '@angular/router';

import { CategoryService } from '../../../admin/admin-categories/categories.service';
import { CategoryData } from '../../interfaces/category.interfaces';

@Component({
  selector: 'app-main-layout',
  imports: [
    FooterComponent,
    HeaderComponent,
    RouterOutlet
  ],
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.scss'
})
export class MainLayoutComponent {
  private categoryService = inject(CategoryService);
  categoryList: CategoryData[] = [];

  ngOnInit(): void {
    this.categoryService.getCategories('').subscribe((data) => {
      this.categoryList = data;
    })
  }
}
