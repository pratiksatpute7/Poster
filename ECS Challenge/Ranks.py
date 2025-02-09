import pandas as pd

def get_top_three_posters(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)
    
    df.rename(columns={df.columns[0]: 'Poster'}, inplace=True)
    
    df_long = df.melt(id_vars=['Poster'], var_name='Judge', value_name='Score')
    
    df_long = df_long[df_long['Score'] > 0]
    
    judge_avg_scores = df_long.groupby('Judge')['Score'].mean()
    overall_avg_score = df_long['Score'].mean()
    
    df_long['Adjusted_Score'] = df_long.apply(lambda row: row['Score'] * (overall_avg_score / judge_avg_scores[row['Judge']]), axis=1)
    
    poster_scores = df_long.groupby('Poster')['Adjusted_Score'].mean().round().astype(int)
    
    top_posters = poster_scores.sort_values(ascending=False)
    
    top_three = top_posters.head(3)
    
    def break_tie(scores, original_scores):
        ranked_posters = scores.index.tolist()
        final_ranking = []
        skip_next = False
        
        for i in range(len(ranked_posters)):
            if skip_next:
                skip_next = False
                continue
            
            if i < len(ranked_posters) - 1 and scores.iloc[i] == scores.iloc[i + 1]:
                # Compare original scores
                poster1, poster2 = ranked_posters[i], ranked_posters[i + 1]
                orig_score1 = original_scores[poster1]
                orig_score2 = original_scores[poster2]
                
                if orig_score1 > orig_score2:
                    final_ranking.append(poster1)
                    final_ranking.append(poster2)
                elif orig_score1 < orig_score2:
                    final_ranking.append(poster2)
                    final_ranking.append(poster1)
                else:
                    final_ranking.append((poster1, poster2))  # Assign same rank if still tied
                
                skip_next = True
            else:
                final_ranking.append(ranked_posters[i])
        
        return final_ranking
    
    original_poster_scores = df_long.groupby('Poster')['Score'].mean().round().astype(int)
    final_ranking = break_tie(top_three, original_poster_scores)
    
    return final_ranking