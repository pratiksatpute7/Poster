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
  code: string = '';
  constructor(private supabaseService: SupabaseService, private router: Router) {}

  async login() {
    const { data, error } = await this.supabaseService.login(this.code);
    if (data) {
      localStorage.setItem('judge', JSON.stringify(data));
      this.router.navigate(['/posters']);
    } else {
      alert('Invalid Code');
    }
  }
}