import { Component, Input, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { DynamicIconComponent } from '../dynamic-icon/dynamic-icon.component';
import { DropdownItems } from '../../interfaces/app.interfaces';

@Component({
  selector: 'app-dropdown',
  imports: [
    CommonModule,
    MatButtonModule,
    DynamicIconComponent
  ],
  templateUrl: './dropdown.component.html',
  styleUrl: './dropdown.component.scss',
  encapsulation: ViewEncapsulation.None
})
export class DropdownComponent {
  @Input() dropdownItems!: DropdownItems;
}
