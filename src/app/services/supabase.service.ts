

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

  async login(code: string) {
    const { data, error } = await this.supabase
      .from('judgeusers')
      .select('*')
      .eq('code', code)
      .single();
    return { data, error };
  }

  async getPostersForJudge(poster_day_id: number) {
    return this.supabase
      .from('posters')
      .select('*')
      .eq('poster_day_id', poster_day_id);
  }

  async submitGrade(judge_id: number, poster_id: number, poster_day_id: number, score: number) {
    return this.supabase
      .from('grades')
      .upsert([{ judge_id, poster_id, poster_day_id, score }]);
  }
}
