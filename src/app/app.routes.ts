import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { PosterListComponent } from './components/poster-list/poster-list.component';
import { GradingComponent } from './components/grading/grading.component';

export const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'posters', component: PosterListComponent },
  { path: 'grading/:id', component: GradingComponent },
  { path: '**', redirectTo: '', pathMatch: 'full' } // Redirect invalid routes
];
