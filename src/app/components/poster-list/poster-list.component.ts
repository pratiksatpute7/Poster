import { Component,OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { SupabaseService } from '../../services/supabase.service';
@Component({
  standalone: true,
  selector: 'app-poster-list',
  templateUrl: './poster-list.component.html',
  styleUrls: ['./poster-list.component.scss'],
  imports:  [CommonModule, MatCardModule, MatButtonModule]
})
export class PosterListComponent implements OnInit {
  posters: any[] = [];

  constructor(private supabaseService: SupabaseService, private router: Router) {}

  async ngOnInit() {
    const judge = JSON.parse(localStorage.getItem('judge') || '{}');
    const { data } = await this.supabaseService.getPostersForJudge(judge.poster_day_id);
    this.posters = data || [];
  }

  gradePoster(posterId: number) {
    this.router.navigate(['/grading', posterId]);
  }
}
