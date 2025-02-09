import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import re

def preprocess_text(text):
    """Preprocess text by converting to lowercase, removing special characters, and stripping whitespace."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)  # Remove special characters
    text = text.strip()
    return text

def filter_posters_with_abstracts(posters_list):
    """Filter out posters that have no abstract."""
    return [poster for poster in posters_list if pd.notna(poster.abstract) and poster.abstract.strip() != ""]

def assign_judges_to_posters(judges_list, posters_list):
    posters_list = filter_posters_with_abstracts(posters_list)  # Filter posters without abstracts
    judge_assignments = []
    poster_assignments = {poster.poster_id: [] for poster in posters_list}
    
    for poster in posters_list:
        relevance_scores = []
        
        for judge in judges_list:
            if len(judge.assigned_posters) >= 6:
                continue  # Skip judges who have already been assigned 6 posters
            
            if (judge.availability != "both") and poster.time_slot != judge.availability:
                continue  # Skip judges with conflicting availability
            
            if poster.advisor_name in judge.name:
                continue  # Skip if there's an advisor conflict
            
            # Compute similarity score
            judge_profile = preprocess_text(str(judge.profile_details)) if pd.notna(judge.profile_details) else ""
            poster_abstract = preprocess_text(str(poster.abstract)) if pd.notna(poster.abstract) else ""
            
            if judge_profile and poster_abstract:
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform([judge_profile, poster_abstract])
                similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            else:
                similarity_score = 0.0
            
            relevance_scores.append((judge, similarity_score))
        
        # Sort judges based on similarity score (highest first)
        relevance_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Assign top 2 judges
        best_judges = relevance_scores[:2]
        for judge, score in best_judges:
            judge.assign_poster(poster.poster_id)
            poster.judges.append(judge.judge_id)
        
        judge_assignments.append({
            'Poster #': poster.poster_id,
            'Poster Title': poster.title,
            'Judge-1 ID': best_judges[0][0].judge_id if len(best_judges) > 0 else None,
            'Judge-1 Name': best_judges[0][0].name if len(best_judges) > 0 else None,
            'Judge-1 Similarity Score': best_judges[0][1] if len(best_judges) > 0 else None,
            'Judge-2 ID': best_judges[1][0].judge_id if len(best_judges) > 1 else None,
            'Judge-2 Name': best_judges[1][0].name if len(best_judges) > 1 else None,
            'Judge-2 Similarity Score': best_judges[1][1] if len(best_judges) > 1 else None
        })
        poster_assignments[poster.poster_id] = [j[0].judge_id for j in best_judges]
    
    # Convert assignments to DataFrame and print
    assignments_df = pd.DataFrame(judge_assignments)
    print(assignments_df.to_string(index=False))
    
    return judge_assignments, poster_assignments