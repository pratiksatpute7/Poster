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
  
  posters = signal<any[]>([]);
  posterId = signal<number | null>(null);
  score = signal<number | null>(null);
  comments = signal('');
  message = signal('');
  judgeId = signal<number | null>(null);

  constructor(private supabaseService: SupabaseService) {}

  async ngOnInit() {
    this.judgeId.set(Number(localStorage.getItem('loggedInJudge')));
    if (!this.judgeId()) {
      this.message.set('You must be logged in to grade posters.');
      return;
    }

    const { data, error } = await this.supabaseService.getPosters();
    if (!error) this.posters.set(data);
  }

  async submitGrade() {
    if (!this.judgeId() || !this.posterId() || !this.score()) {
      this.message.set('Please fill all fields.');
      return;
    }

    const result = await this.supabaseService.addPosterGrade(this.judgeId()!, this.posterId()!, this.score()!);
    this.message.set(result.message);
  }
}