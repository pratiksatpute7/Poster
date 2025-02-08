import { Routes } from '@angular/router';
import { OneComponent } from './one/one.component';

export const routes: Routes = [
    { path: '', component: OneComponent },
    { path: 'about', component: OneComponent },
    { path: 'projects', component: OneComponent },
    { path: 'contact', component: OneComponent },
    { path: '**', redirectTo: '', pathMatch: 'full' } // Redirect unknown paths to home
  ];