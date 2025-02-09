from supabase import create_client, Client
import os
import pandas as pd

# Supabase Setup

SUPABASE_URL = 'https://osumuoaptolaxtzppegj.supabase.co'
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zdW11b2FwdG9sYXh0enBwZWdqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwMzc5MzgsImV4cCI6MjA1NDYxMzkzOH0.onV3HKYPsfC2AAItklWLpkcGz4HHGJJEIjMsujGiuBY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_poster_day(date):
    """Insert a new poster day."""
    data = {"date": date}
    response = supabase.table("posterday").insert(data).execute()
    print("Poster Day inserted:", response)
    return response.data[0]['id'] if response.data else None

def insert_judges(judges_list, poster_day_id):
    """Insert judges into the judgeusers table."""
    data = [{
        "judge": judge.judge_id,
        "judge_firstname": judge.first_name,
        "judge_lastname": judge.last_name,
        "department": judge.department,
        "hour_available": str(judge.availability),
        "code": judge.code,
        "poster_day_id": poster_day_id
    } for judge in judges_list]
    response = supabase.table("judgeusers").insert(data).execute()
    print("Judges inserted:", response)

def insert_posters(posters_list, poster_day_id):
    """Insert posters into the posters table."""
    
    data = []
    for poster in posters_list:
        if(poster.title != ''):
            data.append({
                "id": int(poster.poster_id) if not pd.isna(poster.poster_id) else None,
                "title": str(poster.title) if pd.notna(poster.title) else "",
                "abstract": str(poster.abstract) if pd.notna(poster.abstract) else "",
                "advisor_name": str(poster.advisor_name) if pd.notna(poster.advisor_name) else "",
                "poster_day_id": int(poster_day_id) if not pd.isna(poster_day_id) else None
            })

    response = supabase.table("posters").insert(data).execute()
    print("Posters inserted:", response)


def insert_grades(judge_assignments, poster_day_id):
    """Insert grades into the grades table, ensuring each judge-poster combination is recorded separately."""
    
    data = []
    for grade in judge_assignments:
        if grade["Judge-1 ID"]:
            data.append({
                "judge_id": grade["Judge-1 ID"],
                "poster_id": grade["Poster #"],
                "score": grade.get("Judge-1 Similarity Score", 0),
                "poster_day_id": poster_day_id
            })
        
        if grade["Judge-2 ID"]:
            data.append({
                "judge_id": grade["Judge-2 ID"],
                "poster_id": grade["Poster #"],
                "score": grade.get("Judge-2 Similarity Score", 0),
                "poster_day_id": poster_day_id
            })

    response = supabase.table("grades").insert(data).execute()
    print("Grades inserted:", response)


# Example Usage
# poster_day_id = insert_poster_day("2024-06-01")
# insert_judges(judges_list, poster_day_id)
# insert_posters(posters_list, poster_day_id)
# insert_grades(grades_list, poster_day_id)
