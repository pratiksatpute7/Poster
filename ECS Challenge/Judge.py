import pandas as pd

class Judge:
    def __init__(self, judge_id, first_name, last_name, full_name, availability, profile_details='', emailID=''):
        self.judge_id = judge_id
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.name = full_name
        #self.department = department
        self.availability = availability  # 1, 2, or "both"
        self.assigned_posters = []  # List of assigned poster IDs # List of assigned poster IDs
        self.profile_details = profile_details
        self.emailID = ''
        self.key = ''
        self.competitionID = 0

    def can_review(self, poster):
        """
        Check if the judge can review a given poster based on constraints.
        """
        # Constraint: Each judge can review at most 6 posters
        if len(self.assigned_posters) >= 6:
            return False

        # Constraint: Judge availability should match poster time slot
        if poster.time_slot not in [self.availability, "both"]:
            return False

        # Constraint: A judge cannot review their own student's poster (advisor conflict)
        if poster.advisor_name in self.name:
            return False

        return True

    def assign_poster(self, poster_id):
        """
        Assign a poster to the judge.
        """
        self.assigned_posters.append(poster_id)


def create_judges_list(df):
    judges_list = []
    for _, row in df.iterrows():
        judge = Judge(
            judge_id = row["Email"] if "Email" in df.columns else row["FullName"],
            first_name = row['First Name'].strip(),
            last_name = row['Last Name'].strip(),
            full_name = f"{row['First Name'].strip()} {row['Last Name'].strip()}",
            #department = row["Department"]
            availability = row["Availability"],
            profile_details = row.get("Entry Content", ""),
            emailID = row.get("Email", ""),
        )
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




def display_judges(judges_list):
    print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Department':<10} {'Availability':<10} {'Email ID':<25}")
    print("-" * 120)
    for judge in judges_list:
        print(f"{judge.judge_id:<5} {judge.first_name:<15} {judge.last_name:<15} {judge.availability:<10} {judge.emailID:<25}")
