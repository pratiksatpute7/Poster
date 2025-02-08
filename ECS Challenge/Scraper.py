import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

class ECSFacultyScraper:
    BASE_URL = "https://ecs.syracuse.edu/faculty-staff/"

    def __init__(self):
        self.faculty_data = []

    def scrape_faculty_profiles(self):
        """
        Scrapes faculty profile names and their URLs.
        """
        print(f"Fetching: {self.BASE_URL}")
        try:
            response = requests.get(self.BASE_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Find all faculty profile divs
                faculty_profiles = soup.find_all("div", class_="ecs-profile box-clickable")

                for profile in faculty_profiles:
                    anchor_tag = profile.find("a")  # Find the <a> tag within the div
                    if anchor_tag:
                        name = anchor_tag.text.strip()  # Extract name from anchor text
                        profile_url = anchor_tag["href"]  # Extract href attribute (URL)

                        # Store the extracted data
                        self.faculty_data.append({
                            "FullName": name,
                            "URL": profile_url
                        })

                print(f"Scraped {len(self.faculty_data)} faculty profiles successfully.")

            else:
                print(f"Failed to fetch {self.BASE_URL} (Status Code: {response.status_code})")

        except requests.exceptions.RequestException as e:
            print(f"Error scraping {self.BASE_URL}: {e}")

    def scrape_entry_content(self):
        """
        Visits each faculty profile page and extracts text from <div class="entry-content">.
        Also extracts Syracuse University emails (ending with '@syr.edu').
        """
        for faculty in self.faculty_data:
            url = faculty.get("URL", "")
            if not url.startswith("http"):  # Ensure full URL
                url = "https://ecs.syracuse.edu" + url

            print(f"Scraping entry content: {url}")
            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Extract entry content text
                    entry_content_div = soup.find("div", class_="entry-content")
                    entry_content_text = entry_content_div.get_text(separator=" ").strip() if entry_content_div else "N/A"

                    # Extract email (assumes format like 'xyz@syr.edu')
                    email_match = re.search(r"[a-zA-Z0-9._%+-]+@syr\.edu", response.text)
                    email = email_match.group(0) if email_match else "N/A"

                    # Add scraped text and email to the dictionary
                    faculty["Entry Content"] = entry_content_text
                    faculty["Email"] = email

                else:
                    print(f"Failed to fetch {url} (Status Code: {response.status_code})")
                    faculty["Entry Content"] = "Failed to load"
                    faculty["Email"] = "N/A"

            except requests.exceptions.RequestException as e:
                print(f"Error scraping {url}: {e}")
                faculty["Entry Content"] = "Error"
                faculty["Email"] = "N/A"

            time.sleep(1)  # Delay to avoid getting blocked

    def split_full_name(self, full_name):
        """
        Splits a full name into first, middle, and last names.

        Args:
            full_name (str): The full name of the person.

        Returns:
            dict: A dictionary with 'First Name', 'Middle Name', and 'Last Name'.
        """
        name_parts = full_name.strip().split(" ")

        if len(name_parts) == 1:
            return {"First Name": name_parts[0], "Middle Name": "", "Last Name": ""}
        elif len(name_parts) == 2:
            return {"First Name": name_parts[0], "Middle Name": "", "Last Name": name_parts[1]}
        else:
            return {
                "First Name": name_parts[0],
                "Middle Name": " ".join(name_parts[1:-1]),  # Middle name(s)
                "Last Name": name_parts[-1]
            }

    def process_names(self):
        """
        Splits 'FullName' into 'First Name', 'Middle Name', and 'Last Name'.
        """
        for faculty in self.faculty_data:
            name_split = self.split_full_name(faculty["FullName"])
            faculty.update(name_split)  # Add split names to the dictionary

    def save_to_csv(self, filename="faculty_profiles_with_emails.csv"):
        """
        Saves the updated faculty list (with entry content, name split, and emails) to a CSV file.
        """
        df = pd.DataFrame(self.faculty_data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def run(self):
        """
        Run the scraper: Extract faculty profiles, scrape entry content, extract emails, split names, and save data.
        """
        self.scrape_faculty_profiles()
        self.scrape_entry_content()
        self.process_names()  # Split names
        self.save_to_csv()

# Run the scraper
scraper = ECSFacultyScraper()
scraper.run()
