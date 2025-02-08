import pandas as pd
import Judge
import Poster
from Poster import load_posters_from_csv, assign_judges_to_posters, generate_assignment_matrix, generate_extended_judge_list, generate_extended_poster_list

def main():
    """
    Main function to load the judge and poster data, assign judges to posters, 
    generate assignments, and save the results to an Excel file.
    """
    # Define file paths for judges and posters CSV files
    judges_file = "faculty_profiles_with_emails.csv"  # Ensure this matches your file
    posters_file = "Sample_input_abstracts.csv"  # Ensure this matches your file
    
    # Load judge data from CSV
    df_judges = pd.read_csv(judges_file)
    print("columns in df judges : "+df_judges.columns)
    
    # Create the list of judges
    judges_list = Judge.create_judges_list(df_judges)
    Judge.display_judges(judges_list)  # Optionally display the judges list
    
    # Load poster data
    poster_list = load_posters_from_csv(posters_file)
    posters_df = pd.DataFrame(poster_list)

    judge_assignments, poster_assignments = assign_judges_to_posters(df_judges, posters_df)

    # Generate extended judge and poster lists based on assignments
    extended_judge_list = generate_extended_judge_list(df_judges, judge_assignments)
    extended_poster_list = generate_extended_poster_list(poster_list, poster_assignments)

    # Generate assignment matrix for saving
    assignment_matrix = generate_assignment_matrix(df_judges, poster_assignments)

    # Save the results to an Excel file
    with pd.ExcelWriter('judge_assignments_output.xlsx') as writer:
        extended_judge_list.to_excel(writer, sheet_name='Judge Assignments', index=False)
        extended_poster_list.to_excel(writer, sheet_name='Poster Assignments', index=False)
        assignment_matrix.to_excel(writer, sheet_name='Assignment Matrix', index=False)

    print("Assignment completed and output saved to 'judge_assignments_output.xlsx'.")

if __name__ == "__main__":
    main()
