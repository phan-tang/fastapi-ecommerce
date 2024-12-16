import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatBadgeModule } from '@angular/material/badge';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

import { IconLink } from '../../interfaces/app.interfaces';

@Component({
  selector: 'app-dynamic-icon',
  imports: [
    MatIconModule,
    MatBadgeModule,
    CommonModule
  ],
  templateUrl: './dynamic-icon.component.html',
  styleUrl: './dynamic-icon.component.scss',
})
export class DynamicIconComponent {
  @Input() svgIcon!: IconLink;
  badgeValue: number = -1;

  constructor(private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
    this.iconRegistry.addSvgIcon(this.svgIcon.name,
      this.sanitizer.bypassSecurityTrustResourceUrl(`./icons/${this.svgIcon.iconLink}.svg`)
    );

    this.badgeValue = this.svgIcon.badge ? this.svgIcon.badge : -1;
  }
}
