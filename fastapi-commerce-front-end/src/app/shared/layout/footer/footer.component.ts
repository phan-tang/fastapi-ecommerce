import { Component, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DynamicIconComponent } from '../../components/dynamic-icon/dynamic-icon.component';
import { appName } from '../../constants/app.constants';
import { appSvgItems, footerSvgItems } from '../../constants/iconLink.constants';

@Component({
  selector: 'app-footer',
  imports: [
    DynamicIconComponent,
    CommonModule
  ],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.scss',
  encapsulation: ViewEncapsulation.None
})
export class FooterComponent {
  appName: string = appName;
  appSvgItems = appSvgItems;
  footerSvgItems = footerSvgItems;
}
