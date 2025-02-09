import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { GradingComponent } from './components/grading/grading.component';
import { NgIf, CommonModule } from '@angular/common';
@Component({
  standalone: true,
  selector: 'app-root',
  template: `
      <nav>
      <a routerLink="/login">Login</a> |
      <a routerLink="/posters" *ngIf="isLoggedIn">Grade Posters</a> |
      <button *ngIf="isLoggedIn" (click)="logout()">Logout</button>
    </nav>
  <router-outlet></router-outlet>`,
  imports: [RouterOutlet, GradingComponent, NgIf, CommonModule]
})
export class AppComponent {
  isLoggedIn = localStorage.getItem('loggedInJudge') !== null;

  constructor(private router: Router) {}

  logout() {
    localStorage.removeItem('loggedInJudge');
    this.isLoggedIn = false;
    this.router.navigate(['/login']);
  }
}
