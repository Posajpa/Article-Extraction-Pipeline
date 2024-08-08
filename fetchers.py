from gdeltdoc import GdeltDoc, Filters


def gdelt_fetcher(keyword, start_date, end_date, num_records, domain, domain_exact, country, theme, near, repeat):
    """
    Fetch articles from GDELT based on the specified filters.

    Args:
        keyword (str or list of str): The keyword(s) to search for in articles. Can be a single string or a list of strings.
        start_date (str): The start date for the search range in 'YYYY-MM-DD' format.
        end_date (str): The end date for the search range in 'YYYY-MM-DD' format.
        num_records (int): The number of records to return (up to 250).
        domain (str or list of str, optional): The domain(s) to filter articles by. Can be a single string or a list of strings.
        domain_exact (bool, optional): Whether to match the domain exactly (True) or not (False).
        country (str, optional): The FIPS 2-letter country code to filter articles by.
        theme (str or list of str, optional): The theme(s) to filter articles by. Can be a single string or a list of strings.
        near (str, optional): Construct a filter for words close to each other in the text. Use `near()` to construct.
        repeat (str, optional): Construct a filter for words repeated at least a number of times. Use `repeat()` or `multi_repeat()` to construct.

    Returns:
        list: A list of articles fetched from GDELT matching the filters.
    """
    # Create an instance of the GdeltDoc class
    gd = GdeltDoc()

    # Set filters for the search
    f = Filters(
        keyword=keyword,
        start_date=start_date,
        end_date=end_date,
        num_records=num_records,
        domain=domain,
        domain_exact=domain_exact,
        country=country,
        theme=theme,
        near=near,
        repeat=repeat
    )

    # Perform the article search using the filters
    fetched_articles = gd.article_search(f)

    return fetched_articles


def fetch_articles(keyword, search_parameters, start_date_str, end_date_str):
    """
    Fetch articles based on keyword and search parameters.

    Args:
        keyword (str or list of str): The keyword(s) to search for in articles. Can be a single string or a list of strings.
        search_parameters (dict): Dictionary containing additional search parameters. Keys include:
            - 'num_records': Number of records to return.
            - 'domain': Domain(s) to filter articles by.
            - 'domain_exact': Whether to match the domain exactly.
            - 'country': FIPS 2-letter country code to filter articles by.
            - 'theme': Theme(s) to filter articles by.
            - 'near': Filter for words close to each other in the text.
            - 'repeat': Filter for words repeated at least a number of times.
        start_date_str (str): The start date for the search range in 'YYYY-MM-DD' format.
        end_date_str (str): The end date for the search range in 'YYYY-MM-DD' format.

    Returns:
        list: A list of articles fetched from GDELT based on the provided parameters.
    """
    # Extract search parameters from the dictionary
    num_records = search_parameters.get('num_records')
    domain = search_parameters.get('domain')
    domain_exact = search_parameters.get('domain_exact')
    country = search_parameters.get('country')
    theme = search_parameters.get('theme')
    near = search_parameters.get('near')
    repeat = search_parameters.get('repeat')

    # Call the gdelt_fetcher function to search for articles
    fetched_articles = gdelt_fetcher(keyword, start_date_str, end_date_str, num_records, domain, domain_exact, country, theme, near, repeat)

    # Print the number of articles fetched
    print(f"{len(fetched_articles)} Articles Fetched")

    return fetched_articles
