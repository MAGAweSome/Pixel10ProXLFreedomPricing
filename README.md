# Freedom Mobile Web Scraper

This script scrapes the Freedom Mobile website to retrieve pricing information for the Google Pixel 10 Pro XL and sends it to a Discord channel.

## Prerequisites

- Python 3.x
- The following Python packages:
    - `selenium`
    - `webdriver-manager`
    - `beautifulsoup4`
    - `requests`
    - `python-dotenv`
    - `discord.py`

## Installation

1. Clone the repository.
2. Create a `.env` file by copying the `example.env` file:

```bash
cp example.env .env
```

3. Open the `.env` file and replace the placeholder values with your actual Discord webhook URL, bot token, and channel ID.
4. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, execute the following command:

```bash
python scraper.py
```

The script will then print the pricing information to the console and send it to your Discord channel if the information has changed since the last message.
