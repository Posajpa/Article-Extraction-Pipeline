import yaml
import sys
from fetchers import fetch_articles
from checkers import check_articles
from scrapers import scrape_articles
from datetime import datetime, timedelta
from mongodb import save_to_mongodb
import time


def run_article_extraction(topic, keywords, search_parameters, uri):
    """
    Continuously extracts articles based on keywords and parameters.
    Initially processes data from the past 5 years. After the first run,
    it sleeps for a day and then processes the previous day.

    Args:
        topic (str): The topic for categorizing saved data.
        keywords (list): List of keywords to search for.
        search_parameters (dict): Parameters for fetching articles.
        uri (str): MongoDB URI for saving data.
    """
    init = True  # Flag to indicate whether this is the initial run

    while True:
        print("------------------------------------------------------------")
        print(f"Running Article Extraction")
        start_time = time.time()

        # Loop through each keyword
        for keyword in keywords:
            # Set the start date based on whether it's the initial run
            if init:
                # For the initial run, process articles from 5 years ago
                start_date = datetime.now() - timedelta(days=5*365)
            else:
                # For subsequent runs, process only the previous day
                start_date = datetime.now() - timedelta(days=1)

            # Loop through each day until the start date is today
            while start_date < datetime.now():
                end_date = start_date + timedelta(days=1)

                # Convert datetime to the required string format 'YYYY-MM-DD'
                start_date_str = start_date.strftime('%Y-%m-%d')
                end_date_str = end_date.strftime('%Y-%m-%d')

                print("------------------------------------------------------------")
                print(f"Topic: {topic} / Keyword: {keyword} / Date: {start_date_str}")
                print("------------------------------------------------------------")

                try:
                    # Fetch articles based on the keyword and date range
                    print("Fetching News Articles")
                    fetched_articles = fetch_articles(keyword, search_parameters, start_date_str, end_date_str)
                    save_to_mongodb(fetched_articles, "fetched", topic, keyword, start_date_str, uri)

                    # Check if the fetched articles are allowed based on robots.txt
                    print("Checking Robots.txt Files")
                    approved_articles = check_articles(fetched_articles)
                    save_to_mongodb(approved_articles, "approved", topic, keyword, start_date_str, uri)

                    # Scrape additional details from approved articles
                    print("Scraping Approved Articles")
                    scraped_articles = scrape_articles(approved_articles)
                    save_to_mongodb(scraped_articles, "scraped", topic, keyword, start_date_str, uri)

                except Exception as e:
                    # Handle errors and exit if something goes wrong
                    print(f"Error: {e}")
                    exit(1)

                # Move to the next day
                start_date = end_date

        # Calculate and print the elapsed time for the execution
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("------------------------------------------------------------")
        print("Article Extraction Completed")
        print(f"Duration: {elapsed_time / 60:.2f} minutes.")
        print("Next Article Extraction In 24 Hours")
        print("------------------------------------------------------------")

        # Sleep for 24 hours before the next run
        time.sleep(24 * 60 * 60)

        # Set the flag to False after the initial run
        init = False


def main():
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python main.py <config_file> <key_file>")
        sys.exit(1)

    # Load configuration file
    config_path = sys.argv[1]
    with open(config_path, 'r') as file:
        config_file = yaml.safe_load(file)
    topic = config_file['topic']
    keywords = config_file['keywords']
    search_parameters = config_file['search_parameters']

    # Load key file for MongoDB URI
    key_path = sys.argv[2]
    with open(key_path, 'r') as file:
        key_file = yaml.safe_load(file)
    uri = key_file['mongodb']['uri']

    # Run the article extraction function with loaded parameters
    run_article_extraction(topic, keywords, search_parameters, uri)


if __name__ == "__main__":
    main()
