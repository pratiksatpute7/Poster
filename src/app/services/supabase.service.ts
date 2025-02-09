import { Injectable } from '@angular/core';
import { createClient, SupabaseClient } from '@supabase/supabase-js';

@Injectable({
  providedIn: 'root',
})
export class SupabaseService {
  private supabase: SupabaseClient;

  constructor() {
    this.supabase = createClient(
      'https://osumuoaptolaxtzppegj.supabase.co', // Replace with your Supabase URL
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zdW11b2FwdG9sYXh0enBwZWdqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwMzc5MzgsImV4cCI6MjA1NDYxMzkzOH0.onV3HKYPsfC2AAItklWLpkcGz4HHGJJEIjMsujGiuBY' // Replace with your Supabase anon key
    );
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
}