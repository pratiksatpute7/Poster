import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  standalone: true,
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  imports: [FormsModule, MatCardModule, MatInputModule, MatButtonModule]
})
export class LoginComponent {
  email: string = '';
  secretCode: string = '';

  constructor(private router: Router) {}

  login() {
    if (this.email && this.secretCode) {
      localStorage.setItem('judgeEmail', this.email);
      this.router.navigate(['/posters']);
    } else {
      alert('Please enter valid credentials');
    }
  }
}
