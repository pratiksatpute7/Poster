from ECSFacultyDataDump import get_ecs_dump_data
import Judge
from Poster import load_posters_from_csv

file_path = "Example_list_judges.xlsx"
df_judges = Judge.load_judges_from_excel(file_path)

# Create and display judges list
judges_list = Judge.create_judges_list(df_judges)
Judge.display_judges(judges_list)

file_path = "Sample_input_abstracts.xlsx"
poster_list = load_posters_from_csv(file_path)


csv_filename = "faculty_profiles_with_emails.csv"  # Ensure this matches your saved CSV filename
faculty_list = get_ecs_dump_data(csv_filename)



def update_judges_with_details(judges_list, details_list):
    for judge in judges_list:
        if(judge.judge_id == 3):
            print("hi")
        for detail in details_list:
            if judge.first_name == detail["First Name"] or judge.last_name == detail["Last Name"]:
                print(judge.first_name)
                judge.profile_details = detail.get("Entry Content", "")
                judge.emailID = detail.get("Email", "")
                break
    
    return judges_list

judges_list = update_judges_with_details(judges_list, faculty_list)

Judge.display_judges(judges_list)

print(judges_list[37].first_name)