
    """
    robots_url = urllib.parse.urljoin(url, '/robots.txt')
    rp = urllib.robotparser.RobotFileParser()

    try:
        with urllib.request.urlopen(robots_url, timeout=timeout) as response:
            robots_txt = response.read().decode('utf-8')
            rp.parse(robots_txt.splitlines())
    except Exception as e:
        # Log the error if needed
        # print(f"Error: {e}")
        return False

    return rp.can_fetch(user_agent, url)


def check_articles(fetched_articles):
    """
    Check each article URL to see if it's allowed to be scraped according to robots.txt.

    Args:
        fetched_articles (pd.DataFrame): DataFrame containing article URLs.

    Returns:
        pd.DataFrame: DataFrame containing only the approved articles.
    """
    def process_row(row):
        url = row.url  # Access URL from named tuple
        if robots_checker(url):
            return row._asdict()  # Convert named tuple to dictionary

    # Use ThreadPoolExecutor to process rows in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_row, fetched_articles.itertuples(index=False)))

    # Filter out None results and create DataFrame
    approved_articles = [result for result in results if result is not None]
    approved_articles_df = pd.DataFrame(approved_articles)

    print(f"{len(approved_articles_df)} Articles Approved")

    return approved_articles_df
