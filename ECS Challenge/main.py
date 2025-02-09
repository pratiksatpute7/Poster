from ECSFacultyDataDump import get_ecs_dump_data
import Judge
import database
from Poster import load_posters_from_csv
from assign import assign_judges_to_posters

file_path = "Example_list_judges.xlsx"
df_judges = Judge.load_judges_from_excel(file_path)

# Create and display judges list
judges_list = Judge.create_judges_list(df_judges)
# Judge.display_judges(judges_list)

file_path = "Sample_input_abstracts.xlsx"
poster_list = load_posters_from_csv(file_path)


csv_filename = "faculty_profiles_with_emails.csv"  # Ensure this matches your saved CSV filename
faculty_list = get_ecs_dump_data(csv_filename)


def update_judges_with_details(judges_list, details_list):
    for judge in judges_list:

        for detail in details_list:
            if judge.first_name == detail["First Name"] or judge.last_name == detail["Last Name"]:
                # print(judge.first_name)
                judge.profile_details = detail.get("Entry Content", "")
                judge.emailID = detail.get("Email", "")
                break
    
    return judges_list

# judges_list = update_judges_with_details(judges_list, faculty_list)


# assign_judges_to_posters(judges_list, poster_list)

date = "2024-06-01"  # Example date, change as needed
poster_day_id = database.insert_poster_day(date)
database.insert_judges(judges_list, poster_day_id)
database.insert_posters(poster_list, poster_day_id)

# Assign judges to posters and insert grades
judge_assignments, poster_assignments = assign_judges_to_posters(judges_list, poster_list)
database.insert_grades(judge_assignments, poster_day_id)