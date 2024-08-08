from newspaper import Article
import pandas as pd
import concurrent.futures


def newspaper3k_scraper(url):
    """
    Scrape article data from a given URL using the newspaper3k library.

    Args:
        url (str): The URL of the article to scrape.

    Returns:
        dict: A dictionary containing article data or None if an error occurs.
    """
    url = url.strip()
    article = Article(url)
    try:
        article.download()
        article.parse()
        article.nlp()
        return {
            'title': article.title,
            'authors': article.authors,
            'publish_date': article.publish_date.isoformat() if article.publish_date else None,
            'text': article.text,
            'summary': article.summary,
            'keywords': article.keywords,
            'source_url': article.source_url,
            'image_url': article.top_image
        }
    except Exception as e:
        # Log the error if needed
        # print(f"Error: {e}")
        return None


def scrape_articles(approved_articles):
    """
    Scrape articles in parallel from a DataFrame of approved article URLs.

    Args:
        approved_articles (pd.DataFrame): DataFrame containing approved article URLs.

    Returns:
        pd.DataFrame: DataFrame containing the scraped articles.
    """
    def process_row(row):
        url = row.url  # Access URL from named tuple
        data = newspaper3k_scraper(url)
        return data

    # Use ThreadPoolExecutor to process rows in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_row, approved_articles.itertuples(index=False)))

    # Filter out None results and create DataFrame
    scraped_articles = [result for result in results if result is not None]
    scraped_articles_df = pd.DataFrame(scraped_articles)

    print(f"{len(scraped_articles_df)} Articles Scraped")

    return scraped_articles_df
