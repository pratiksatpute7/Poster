import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';

@Component({
  standalone: true,
  selector: 'app-poster-list',
  templateUrl: './poster-list.component.html',
  styleUrls: ['./poster-list.component.scss'],
  imports:  [CommonModule, MatCardModule, MatButtonModule]
})
export class PosterListComponent {
  posters = [
    { id: 1, title: 'Poster 1', abstract: 'Abstract about topic 1' },
    { id: 2, title: 'Poster 2', abstract: 'Abstract about topic 2' },
    { id: 3, title: 'Poster 3', abstract: 'Abstract about topic 3' }
  ];

  constructor(private router: Router) {}

  gradePoster(id: number) {
    this.router.navigate(['/grading', id]);
  }

  submitScores() {
    alert('Scores submitted successfully!');
  }
}
