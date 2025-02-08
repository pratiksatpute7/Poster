import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Judge import create_judges_list



class Poster:
    def __init__(self, poster_id, title, abstract, advisor_first, advisor_last, program):
        self.poster_id = poster_id
        self.title = title
        self.abstract = abstract
        self.advisor_name = f"{advisor_first} {advisor_last}"
        self.advisor_first = advisor_first
        self.advisor_second = advisor_last
        self.program = program
        self.judges = []  # List of assigned judges
        self.time_slot = 1 if poster_id % 2 != 0 else 2  # Odd = Slot 1, Even = Slot 2

    def calculate_relevance_score(self, judge):
        """
        Calculate the relevance score between a judge and a poster.
        Uses cosine similarity between the judge's research area and the poster's abstract.
        
        Args:
            judge (Judge): The judge object whose research area will be compared to the poster's abstract.
        
        Returns:
            float: The relevance score between the judge's research area and the poster's abstract (0 to 1 scale).
        """
        # Ensure judge's research area and poster's abstract are strings
        judge_research_area = str(judge.profile_details) if pd.notna(judge.profile_details) else ""
        poster_abstract = str(self.abstract) if pd.notna(self.abstract) else ""

        # If both strings are empty, return zero similarity
        if not judge_research_area.strip() or not poster_abstract.strip():
            return 0.0

        # Create a TfidfVectorizer to convert text to numerical representations (TF-IDF vectors)
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')

        # Fit and transform both the judge's research area and the poster's abstract
        tfidf_matrix = tfidf_vectorizer.fit_transform([judge_research_area, poster_abstract])

        # Compute the cosine similarity between the judge's research area and the poster's abstract
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        # Return the cosine similarity score as the relevance score
        return cosine_sim[0][0]


    def assign_judge(self, judge_id):
        """
        Assign a judge to this poster.
        """
        self.judges.append(judge_id)

def load_posters_from_csv(file_path):
    df = pd.read_csv(file_path)
    posters_list = []
    for _, row in df.iterrows():
        poster = Poster(
            poster_id=row["Poster #"],
            title=row["Title"],
            abstract=row["Abstract"],
            advisor_first=row["Advisor FirstName"],
            advisor_last=row["Advisor LastName"],
            program=row["Program"]
        )
        posters_list.append(poster)
    return df



# def get_best_two_judges(self, judges_list):
#         """
#         Select the best two judges for the poster based on relevance scores.
#         Returns the IDs of the best two judges.
        
#         Args:
#             judges_list (dict): A dictionary of judge objects.
        
#         Returns:
#             list: A list containing the IDs of the top two judges.
#         """
#         # Calculate relevance score for each judge
#         relevance_scores = {}
#         for judge_id, judge in judges_list.items():
#             score = self.calculate_relevance_score(judge)
#             relevance_scores[judge_id] = score

#         # Sort judges by relevance score in descending order
#         sorted_judges = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)

#         # Select the top two judges based on relevance score
#         top_two_judges = [judge_id for judge_id, _ in sorted_judges[:2]]

#         return top_two_judges


# def assign_judges_to_posters(judges_df, posters_df):
#     judge_assignments = []
#     poster_assignments = {poster_id: [] for poster_id in posters_df['Poster #']}
#     judges_list = create_judges_list(judges_df)
    
#     for _, poster in posters_df.iterrows():
#         relevance_scores = {}
        
#         for judge in judges_list:
#             score = poster.calculate_relevance_score(judge)
#             relevance_scores[judge['Judge']] = score
        
#         # Sort judges by relevance score (highest to lowest)
#         sorted_judges = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
        
#         # Assign the top two judges
#         best_judges = [sorted_judges[0][0], sorted_judges[1][0]]
#         judge_assignments.append({'Poster #': poster['Poster #'], 'Judge-1': best_judges[0], 'Judge-2': best_judges[1]})
        
#         # Update poster assignments
#         poster_assignments[poster['Poster #']] = best_judges
    
#     return judge_assignments, poster_assignments


def assign_judges_to_posters(judges_df, posters_df):
    judge_assignments = []
    poster_assignments = {}

    # Convert DataFrame rows into Poster objects
    posters_list = []
    for _, row in posters_df.iterrows():
        poster = Poster(
            poster_id=row["Poster #"],
            title=row["Title"],
            abstract=row["Abstract"],
            advisor_first=row["Advisor FirstName"],
            advisor_last=row["Advisor LastName"],
            program=row["Program"]
        )
        posters_list.append(poster)
        poster_assignments[poster.poster_id] = []  # Initialize poster assignments

    judges_list = create_judges_list(judges_df)

    for poster in posters_list:  # Iterate over Poster objects
        relevance_scores = {}

        for judge in judges_list:
            score = poster.calculate_relevance_score(judge)  # Now calling on Poster object
            relevance_scores[judge.judge_id] = score  # Ensure correct attribute name

        # Sort judges by relevance score (highest to lowest)
        sorted_judges = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)

        # Assign the top two judges
        if len(sorted_judges) >= 2:  # Ensure at least 2 judges are available
            best_judges = [sorted_judges[0][0], sorted_judges[1][0]]
        elif len(sorted_judges) == 1:  # Fallback in case only 1 judge is found
            best_judges = [sorted_judges[0][0]]
        else:
            best_judges = []  # No suitable judges found

        judge_assignments.append({'Poster #': poster.poster_id, 'Judge-1': best_judges[0] if len(best_judges) > 0 else None, 'Judge-2': best_judges[1] if len(best_judges) > 1 else None})

        # Update poster assignments
        poster_assignments[poster.poster_id] = best_judges

    return judge_assignments, poster_assignments

# def generate_extended_judge_list(judges_df, judge_assignments):
#     judge_list = pd.DataFrame(judges_df)
#     judge_list['Assigned Posters'] = np.nan
    
#     for assignment in judge_assignments:
#         judge_id_1 = assignment['Judge-1']
#         judge_id_2 = assignment['Judge-2']
#         judge_list.loc[judge_list['Judge'] == judge_id_1, 'Assigned Posters'] = judge_list.loc[judge_list['Judge'] == judge_id_1, 'Assigned Posters'].apply(lambda x: f"{x}, {assignment['Poster #']}" if pd.notna(x) else f"{assignment['Poster #']}")
#         judge_list.loc[judge_list['Judge'] == judge_id_2, 'Assigned Posters'] = judge_list.loc[judge_list['Judge'] == judge_id_2, 'Assigned Posters'].apply(lambda x: f"{x}, {assignment['Poster #']}" if pd.notna(x) else f"{assignment['Poster #']}")
    
#     return judge_list

def generate_extended_judge_list(judges_df, judge_assignments):
    # Ensure column names are stripped of spaces
    judges_df.columns = judges_df.columns.str.strip()

    # Verify correct column name
    expected_judge_column = 'Judge' if 'Judge' in judges_df.columns else 'FullName'  # Adjust if needed

    judge_list = pd.DataFrame(judges_df)
    judge_list['Assigned Posters'] = np.nan  # Initialize assigned posters column
    
    for assignment in judge_assignments:
        judge_id_1 = assignment.get('Judge-1', None)
        judge_id_2 = assignment.get('Judge-2', None)

        # Ensure judge IDs exist before assignment
        if judge_id_1 and judge_id_1 in judge_list[expected_judge_column].values:
            judge_list.loc[judge_list[expected_judge_column] == judge_id_1, 'Assigned Posters'] = \
                judge_list.loc[judge_list[expected_judge_column] == judge_id_1, 'Assigned Posters'].apply(
                    lambda x: f"{x}, {assignment['Poster #']}" if pd.notna(x) else f"{assignment['Poster #']}"
                )

        if judge_id_2 and judge_id_2 in judge_list[expected_judge_column].values:
            judge_list.loc[judge_list[expected_judge_column] == judge_id_2, 'Assigned Posters'] = \
                judge_list.loc[judge_list[expected_judge_column] == judge_id_2, 'Assigned Posters'].apply(
                    lambda x: f"{x}, {assignment['Poster #']}" if pd.notna(x) else f"{assignment['Poster #']}"
                )

    return judge_list


def generate_extended_poster_list(posters_df, poster_assignments):
    poster_list = pd.DataFrame(posters_df)
    
    # Add columns for assigned judges
    for i in range(1, 7):  # There can be up to 6 posters assigned to each judge
        poster_list[f"Poster-{i}"] = poster_list['Poster #'].apply(lambda x: poster_assignments[x][i-1] if i <= len(poster_assignments[x]) else np.nan)
    
    return poster_list


# def generate_assignment_matrix(judges_df, poster_assignments):
#     # Create a matrix with posters as rows and judges as columns
#     judge_ids = judges_df['Judge'].tolist()
#     assignment_matrix = pd.DataFrame(np.zeros((len(poster_assignments), len(judge_ids))), columns=judge_ids)
    
#     for poster_id, judges in poster_assignments.items():
#         for judge_id in judges:
#             assignment_matrix.loc[poster_id - 1, judge_id] = 1
    
#     return assignment_matrix


def generate_assignment_matrix(judges_df, poster_assignments):
    # Ensure column names are stripped of spaces
    judges_df.columns = judges_df.columns.str.strip()

    # Determine correct judge column name
    expected_judge_column = 'Judge' if 'Judge' in judges_df.columns else 'FullName'  # Adjust if needed

    # Create a matrix with posters as rows and judges as columns
    judge_ids = judges_df[expected_judge_column].tolist()
    assignment_matrix = pd.DataFrame(np.zeros((len(poster_assignments), len(judge_ids))), columns=judge_ids)

    for poster_id, judges in poster_assignments.items():
        for judge_id in judges:
            if judge_id in assignment_matrix.columns:
                assignment_matrix.loc[poster_id - 1, judge_id] = 1  # Ensure poster_id is valid index

    return assignment_matrix
