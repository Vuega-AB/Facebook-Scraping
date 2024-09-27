# Facebook Scraping with Selenium and Google Custom Search API

This project is a web scraping tool built to extract Facebook reviews and recommendations using **Selenium** for web interaction and **Google Custom Search API** to find specific Facebook pages. The tool automatically navigates to Facebook pages, closes login windows, and fetches user reviews, separating recommendations and non-recommendations. Additionally, it provides functionality to clean and format extracted data by removing unnecessary comments and duplicates.

## Key Features:
- **Google Custom Search Integration:** Uses Google API to search for Facebook pages and specific queries.
- **Selenium Automation:** Automates navigation, login window closure, and review extraction from Facebook pages.
- **Data Cleaning:** Extracts, formats, and removes unnecessary content from the scraped reviews.
- **Headless Mode:** The browser operates in the background, making scraping faster and more efficient.
- **Review Management:** Classifies and stores reviews into 'recommends' and 'doesn't recommend' categories.

## Workflow:
1. Input a search query into the **Streamlit** interface to retrieve Facebook page links using Google Custom Search API.
2. The script navigates to the Facebook page, closes any login pop-ups, and searches for review sections.
3. Reviews are extracted and saved into a file.
4. Comments and reactions are removed from the reviews, and duplicate entries are filtered out.
5. Cleaned reviews are categorized and saved for further analysis or use.

## How to Use:
1. Clone the repository and set up the required dependencies.
2. Input your own **Google Custom Search API Key** and **Search Engine ID**.
3. Run the Streamlit app and enter your search query.
4. The program will automatically navigate to the relevant Facebook page, scrape reviews, and save the output in a cleaned format.

## Requirements:
- Python 3.x
- Selenium
- Streamlit
- Chrome WebDriver
- Google Custom Search API Key

## Installation:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/facebook-scraping.git
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Download Chrome WebDriver and update the path in the script if needed.

## Run the Streamlit App:
```bash
streamlit run app.py
```
