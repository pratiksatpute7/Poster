import pandas as pd
import Judge
import Poster

class AssignmentSystem:
    def __init__(self, judges_df, posters_df):
        self.judges = self._create_judges(judges_df)
        self.posters = self._create_posters(posters_df)

    def _create_judges(self, judges_df):
        """
        Convert judges dataframe into a dictionary of Judge objects.
        """
        judges = {}
        for _, row in judges_df.iterrows():
            judge = Judge(
                judge_id=row["Judge"],
                full_name=row["Full Name"],
                department=row["Department"],
                availability=row["Hour available"],
            )
            judges[judge.judge_id] = judge
        return judges

    def _create_posters(self, posters_df):
        """
        Convert posters dataframe into a dictionary of Poster objects.
        """
        posters = {}
        for _, row in posters_df.iterrows():
            poster = Poster(
                poster_id=row["Poster #"],
                title=row["Title"],
                abstract=row["Abstract"],
                advisor_first=row["Advisor FirstName"],
                advisor_last=row["Advisor LastName"],
                program=row["Program"],
            )
            posters[poster.poster_id] = poster
        return posters

    def display_judges(self):
        """
        Display a summary of judges.
        """
        judge_list = [{"ID": j.judge_id, "Name": j.name, "Department": j.department, "Availability": j.availability} for j in self.judges.values()]
        return pd.DataFrame(judge_list)

    def display_posters(self):
        """
        Display a summary of posters.
        """
        poster_list = [{"ID": p.poster_id, "Title": p.title, "Advisor": p.advisor_name, "Program": p.program} for p in self.posters.values()]
        return pd.DataFrame(poster_list)
