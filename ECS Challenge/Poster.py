import pandas as pd


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

    def assign_judge(self, judge_id):
        """
        Assign a judge to this poster.
        """
        self.judges.append(judge_id)

def load_posters_from_csv(file_path):
    df = pd.read_excel(file_path)
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
    return posters_list