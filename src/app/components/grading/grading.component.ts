import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { MatSliderModule } from '@angular/material/slider';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { NgIf, CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-grading',
  templateUrl: './grading.component.html',
  styleUrls: ['./grading.component.scss'],
  imports: [ReactiveFormsModule, MatSliderModule, MatCardModule, MatButtonModule, NgIf, CommonModule],
})
export class GradingComponent implements OnInit {
  posterTitle: string = '';
  score = new FormControl(3); // Default value is 3

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit() {
    const posterId = this.route.snapshot.paramMap.get('id');
    this.posterTitle = `Poster ${posterId}`;
  }

  // Custom thumb label formatting logic
  formatLabel(value: number): string {
    // Example: You can apply custom logic here. For now, we will just return the number as-is.
    // Modify this to format the value based on the business logic you need.
    if (value === 5) {
      return '5';
    } else if (value === 4) {
      return '4';
    } else if (value === 3) {
      return '3';
    } else if (value === 2) {
      return '2';
    } else {
      return '1';
    }
  }

  submitScore() {
    console.log(`Submitted score: ${this.score.value}`);
    alert(`Submitted score: ${this.score.value}`);
    this.router.navigate(['/posters']);
  }
}
