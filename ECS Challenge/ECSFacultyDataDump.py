import pandas as pd

def get_ecs_dump_data(csv_filename):
    """
    Reads a CSV file and converts it into a list of dictionaries.
    
    Args:
        csv_filename (str): The path to the CSV file.
    
    Returns:
        list: A list of dictionaries, where each dictionary represents a row from the CSV.
    """
    try:
        # Load the CSV file
        df = pd.read_csv(csv_filename)

        # Convert DataFrame to a list of dictionaries
        faculty_list = df.to_dict(orient="records")

        return faculty_list

    except FileNotFoundError:
        print(f"Error: The file '{csv_filename}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
csv_filename = "faculty_profiles.csv"  # Ensure this matches your saved CSV filename
faculty_list = get_ecs_dump_data(csv_filename)

# Print the list of dictionaries
# print(faculty_list)
