import { Component, ViewEncapsulation, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DynamicIconComponent } from '../dynamic-icon/dynamic-icon.component';
import { IconLink } from '../../interfaces/app.interfaces';
import { starFillIcon, starEmptyIcon, starHalfIcon } from '../../constants/iconLink.constants';

@Component({
  selector: 'app-rating-star',
  imports: [
    CommonModule,
    DynamicIconComponent
  ],
  templateUrl: './rating-star.component.html',
  styleUrl: './rating-star.component.scss',
  encapsulation: ViewEncapsulation.None
})
export class RatingStarComponent {
  @Input() rating!: number;
  rating_stars: IconLink[] = [];

  ngOnInit(): void {
    this.generateRating();
  }

  generateRating() {
    let fillStars = Math.floor(this.rating);
    let iconLink = starFillIcon;
    for (let index = 1; index <= 5; index++) {
      if (index > fillStars) {
        iconLink = index === fillStars + 1 && fillStars !== this.rating ? starHalfIcon : starEmptyIcon;
      }
      this.rating_stars.push({ name: iconLink, iconLink })
    }
  }
}
