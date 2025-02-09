import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { SupabaseService } from '../../services/supabase.service';

@Component({
  standalone: true,
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  imports: [FormsModule, MatCardModule, MatInputModule, MatButtonModule],
  providers: [SupabaseService]
})
export class LoginComponent {
  judgeId = signal<number | null>(null);
  secretCode = signal('');
  loginMessage = signal('');

  constructor(private supabaseService: SupabaseService, private router: Router) {}

  async login() {
    if (!this.judgeId() || !this.secretCode()) {
      this.loginMessage.set('Please enter both fields.');
      return;
    }

    const result = await this.supabaseService.loginJudge(this.judgeId()!, this.secretCode());
    this.loginMessage.set(result.message);

    if (result.success) {
      localStorage.setItem('loggedInJudge', this.judgeId()!.toString());
      this.router.navigate(['/poster-list']); // Redirect to dashboard
    }
  }
}