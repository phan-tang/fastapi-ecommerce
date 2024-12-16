import { Component, ViewEncapsulation, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DynamicIconComponent } from '../../components/dynamic-icon/dynamic-icon.component';
import { NavItemComponent } from '../../components/nav-item/nav-item.component';
import { DropdownComponent } from '../../components/dropdown/dropdown.component';
import { appSvgItems, navItems } from '../../constants/iconLink.constants';

import { DropdownItems } from '../../interfaces/app.interfaces';
import { CategoryData } from '../../interfaces/category.interfaces';

@Component({
  selector: 'app-header',
  imports: [
    CommonModule,
    DynamicIconComponent,
    DropdownComponent,
    NavItemComponent
  ],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
  encapsulation: ViewEncapsulation.None
})
export class HeaderComponent {
  @Input() categoryList!: CategoryData[];
  dropdownItems: DropdownItems = {
    buttonDisplay: {
      title: 'Category',
      name: 'Category',
      iconLink: 'category',
    },
    options: []
  };
  appSvgItems = appSvgItems;
  navItems = navItems;

  ngOnInit(): void {
    this.dropdownItems.options = this.categoryList.map((item) => {
      return {
        name: item.category_name.toLowerCase(),
        title: item.category_name,
        id: item.id,
        iconLink: item.icon ? item.icon : 'default',
      };
    })
  }
}
