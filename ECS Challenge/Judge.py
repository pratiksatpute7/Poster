import pandas as pd


class Judge:
    def __init__(self, judge_id, first_name, last_name, full_name, department, availability):
        self.judge_id = judge_id
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.name = full_name
        self.department = department
        self.availability = availability  # 1, 2, or "both"
        self.assigned_posters = []  # List of assigned poster IDs # List of assigned poster IDs
        self.profile_details = ''
        self.emailID = ''
        self.key = ''
        self.competitionID = 0

    def assign_poster(self, poster_id):
        """
        Assign a poster to the judge.
        """
        self.assigned_posters.append(poster_id)


def create_judges_list(df):
    judges_list = []
    for _, row in df.iterrows():
        judge_id = row["Judge"]
        first_name = row['Judge FirstName'].strip()
        last_name = row['Judge LastName'].strip()
        full_name = f"{first_name} {last_name}"
        department = row["Department"]
        availability = row["Hour available"]
        
        judge = Judge(judge_id, first_name, last_name, full_name, department, availability)
        judges_list.append(judge)
    return judges_list

# Function to display judges' details
# def display_judges(judges_list):
#     print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Department':<10} {'Availability':<10}")
#     print("-" * 65)
#     for judge in judges_list:
#         print(f"{judge.judge_id:<5} {judge.first_name:<15} {judge.last_name:<15} {judge.department:<10} {judge.availability:<10}")

def load_judges_from_excel(file_path, sheet_name="Sheet1"):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df




# def display_judges(judges_list):
#     print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Department':<10} {'Availability':<10} {'Email ID':<25}")
#     print("-" * 120)
#     for judge in judges_list:
#         print(f"{judge.judge_id:<5} {judge.first_name:<15} {judge.last_name:<15} {judge.department:<10} {judge.availability:<10} {judge.emailID:<25}")


