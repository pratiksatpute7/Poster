import { Component, OnInit, signal} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatSliderModule } from '@angular/material/slider';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { NgIf, CommonModule } from '@angular/common';
import { SupabaseService } from '../../services/supabase.service';
@Component({
  standalone: true,
  selector: 'app-grading',
  templateUrl: './grading.component.html',
  styleUrls: ['./grading.component.scss'],
  imports: [FormsModule, ReactiveFormsModule, MatSliderModule, MatCardModule, MatButtonModule, NgIf, CommonModule],
  providers: [SupabaseService]
})
export class GradingComponent {
  score: number = 1;
  posterId!: number;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private supabaseService: SupabaseService
  ) {
    this.posterId = Number(this.route.snapshot.paramMap.get('id'));
  }

  async submitGrade() {
    const judge = JSON.parse(localStorage.getItem('judge') || '{}');
    await this.supabaseService.submitGrade(judge.judge, this.posterId, judge.poster_day_id, this.score);
    this.router.navigate(['/posters']);
  }
}
