

import { Injectable } from '@angular/core';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://osumuoaptolaxtzppegj.supabase.co'; // Replace with your actual Supabase URL
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zdW11b2FwdG9sYXh0enBwZWdqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwMzc5MzgsImV4cCI6MjA1NDYxMzkzOH0.onV3HKYPsfC2AAItklWLpkcGz4HHGJJEIjMsujGiuBY'; // Replace with your actual Supabase anon key

@Injectable({
  providedIn: 'root',
})
export class SupabaseService {
  private supabase: SupabaseClient;

  constructor() {
    this.supabase = createClient(supabaseUrl, supabaseAnonKey);
  }

  // Judge Login - Validate Secret Code
  async loginJudge(judgeId: number, enteredSecret: string) {
    const { data, error } = await this.supabase
      .from('judgesecrets')
      .select('secret_code')
      .eq('judge_id', judgeId)
      .single(); // Get a single record

    if (error) {
      console.error('Login error:', error.message);
      return { success: false, message: 'Judge not found' };
    }

    if (data.secret_code === enteredSecret) {
      return { success: true, message: 'Login successful' };
    } else {
      return { success: false, message: 'Invalid secret code' };
    }
  }
  async getPosters() {
    return this.supabase.from('posters').select('*');
  }
  
  // Submit a grade
  async addPosterGrade(judgeId: number, posterId: number, score: number) {
    const { error } = await this.supabase.from('poster_grades').insert([
      { judge_id: judgeId, poster_id: posterId, score: score }
    ]);
  
    if (error) {
      console.error('Grading error:', error.message);
      return { success: false, message: 'Failed to submit grade' };
    }
    return { success: true, message: 'Grade submitted successfully' };
  }
}
