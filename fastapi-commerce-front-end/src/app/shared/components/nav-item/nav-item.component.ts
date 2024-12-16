import { Component, Input, ViewEncapsulation } from '@angular/core';
import { DynamicIconComponent } from '../dynamic-icon/dynamic-icon.component';
import { IconLink } from '../../interfaces/app.interfaces';

@Component({
  selector: 'app-nav-item',
  imports: [
    DynamicIconComponent
  ],
  templateUrl: './nav-item.component.html',
  styleUrl: './nav-item.component.scss',
  encapsulation: ViewEncapsulation.None
})
export class NavItemComponent {
  @Input() navItem!: IconLink;
}
