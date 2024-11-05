import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm import tqdm
import unicodedata

# Define input and output directories
INPUT_FILE = "input/clusters.csv"  # Input file for cluster names and URLs
OUTPUT_FILE = "output/cluster_data_output.csv"  # Output file for scraped data


def clean_text(text):
    """
    Cleans and normalizes the text to remove unwanted special characters.
    """
    # Normalize unicode characters and remove non-printable characters
    text = unicodedata.normalize("NFKD", text)
    # Strip leading and trailing whitespace and return the cleaned text
    return text.strip()


def scrape_cluster_data(cluster_url):
    """
    Scrapes a cluster overview page at the provided URL to extract:
    - Cluster description
    - Cluster video URL
    - Transcript text (if available)

    Parameters:
        cluster_url (str): URL of the cluster page to scrape

    Returns:
        tuple: (description, video_url, transcript)
    """
    # Headers to simulate a request coming from a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Send a GET request to the URL
        response = requests.get(cluster_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for failed requests
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract and clean the description text from the div with class "video-description"
        description_tag = soup.find("div", class_="video-description")
        description = (
            clean_text(description_tag.get_text(strip=True))
            if description_tag
            else "N/A"
        )

        # Extract and clean the video URL from the <video> tag
        video_tag = soup.find("video")
        video_url = video_tag["src"] if video_tag else "N/A"

        # Extract and clean the transcript text from the div with class "video-transcript"
        transcript_tag = soup.find("div", class_="video-transcript")
        transcript = (
            clean_text(transcript_tag.get_text(separator=" ", strip=True))
            if transcript_tag
            else "N/A"
        )

        return description, video_url, transcript

    except requests.RequestException as e:
        print(f"Error fetching {cluster_url}: {e}")
        return "N/A", "N/A", "N/A"


def main():
    """
    Main function to:
    - Read a list of clusters and their URLs from an input CSV file
    - Scrape each cluster page for description, video URL, and transcript
    - Save the scraped data to an output CSV file
    """
    # List to store all scraped data
    cluster_data = []

    # Open the input CSV and read each row (each row contains a cluster name and URL)
    with open(INPUT_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Print headers to verify column names
        print("CSV Headers:", reader.fieldnames)

        rows = list(reader)  # Convert to a list to know the total for the progress bar

        # Loop through each row and scrape data for each cluster URL
        for row in tqdm(rows, desc="Scraping Cluster Data", unit="cluster"):
            # Adjust the column names if they differ in your CSV file
            cluster_name = row.get(
                "Cluster", row.get("Cluster Name", None)
            )  # Cluster name
            cluster_url = row.get("URL", row.get("Cluster URL", None))  # Cluster URL

            if not cluster_name or not cluster_url:
                print("Error: Missing 'Cluster' or 'URL' column in CSV.")
                continue  # Skip this row if required fields are missing

            # Scrape the data for this cluster URL
            description, video_url, transcript = scrape_cluster_data(cluster_url)

            # Add the data as a dictionary to the list
            cluster_data.append(
                {
                    "Cluster Name": cluster_name,
                    "Description": description,
                    "Video URL": video_url,
                    "Transcript": transcript,
                }
            )

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Save the scraped data to the output CSV file
    df = pd.DataFrame(cluster_data)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"Data saved to {OUTPUT_FILE}")


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
