# Article Extraction Pipeline

## Overview

This project automates the extraction, filtering, and scraping of news articles related to specified topics and keywords. It leverages several Python libraries and a MongoDB database to fetch articles, check their availability via `robots.txt`, scrape the content, and store it in a structured format.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](configuration)
- [Usage](usage)
- [How It Works](how-it-works)
- [Code Structure](code-structure)
- [Contributing](contributing)
- [License](license)
- [Contact](contact)
  
## Features

- **Keyword-based Article Search**: Fetch articles related to specific keywords within a defined timeframe.
- **Robots.txt Validation**: Ensure compliance with web scraping rules by checking the `robots.txt` file.
- **Content Scraping**: Extract the title, authors, publish date, text, summary, keywords, and images from articles.
- **MongoDB Integration**: Store fetched, approved, and scraped articles in a MongoDB database.
- **Automated Daily Runs**: After an initial backfill, the pipeline runs daily to collect and store new articles.

## Requirements

- **Python**: 3.7+
- **MongoDB**
- **Python Libraries**:
  - `pymongo`
  - `pandas`
  - `newspaper3k`
  - `concurrent.futures`
  - `yaml`
  - `gdeltdoc`
  - `urllib`

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Posajpa/Article-Extraction-Pipeline.git
    cd article-extraction-pipeline
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up MongoDB:**
   Ensure that your MongoDB instance is running and accessible. Update the MongoDB URI in the following configuration files.

## Configuration

Create a YAML configuration file with the following structure:

```yaml
# ----------------------------------------------
topic: "USA Elections"
# ----------------------------------------------
keywords: [
  - "Trump"
  - "Kamala"
]
# ----------------------------------------------
search_parameters:
  num_records: 250
  domain (optional):
  domain_exact (optional):
  near (optional):
  repeat (optional):
  country (optional):
  theme (optional):
```

Create another YAML file for your MongoDB URI:

```yaml
# ----------------------------------------------
mongodb:
  uri: "your_mongodb_uri_here"
# ----------------------------------------------
```

## Usage

To run the pipeline:

```bash
python main.py <config_file> <key_file>
```

- `<config_file>`: Path to your configuration YAML file.
- `<key_file>`: Path to your MongoDB URI YAML file.

## How It Works

1. The script begins by fetching articles based on the keywords and search parameters provided.
2. It checks the articles against `robots.txt` files to ensure scraping is allowed.
3. Approved articles are scraped, and their content is stored in a MongoDB database.
4. The initial run backfills articles for each day for the past 5 years (or a configurable duration). Subsequent runs only fetch articles from the previous day.

## Code Structure

- `main.py`: The main entry point for the article extraction pipeline.
- `fetchers.py`: Contains the logic for fetching articles using the GDELT API.
- `checkers.py`: Handles robots.txt validation.
- `scrapers.py`: Scrapes content from approved articles using newspaper3k.
- `mongodb.py`: Manages interactions with MongoDB, including saving fetched, approved, and scraped articles.
- `config/`: Contains example configuration files.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Posajpa/Article-Extraction-Pipeline/blob/main/LICENSE) file for details.

## Contact

If you have any questions, please reach out to posajpa@gmail.com.
