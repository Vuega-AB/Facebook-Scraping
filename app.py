import requests
import streamlit as st
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def google_search(query, api_key, search_engine_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': search_engine_id,
    }
    response = requests.get(url, params=params)
    return response.json()

# Replace these with your actual API key and Search Engine ID
api_key = 'AIzaSyAcEhygRJDoBeCBePgPxTxlwWGSXmnGTwo'
search_engine_id = '70fd339e45a0e4b2c'

# Streamlit app layout
st.title("Google Custom Search")
query = st.text_input("Enter your search query:")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def navigate_to_facebook_main_page(driver):
    # Define the class names used for the anchor tag
    class_name_1 = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"
    class_name_2 = "x1i10hfl xe8uvvx xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz xjyslct xjbqb8w x18o3ruo x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g x1ypdohk xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg x1vjfegm x3nfvp2 xrbpyxo x1itg65n x16dsc37"

    # First attempt to find the link with the first class
    try:
        store_link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"a.{class_name_1.replace(' ', '.')}"))
        )
        store_url = store_link_element.get_attribute("href")
        if store_url:
            print(f"Navigating to: {store_url}")
            driver.get(store_url)  # Navigate to the store URL
            return store_url
    except Exception as e:
        print(f"Error finding the store link in the first class: {e}")

    # If the first attempt fails, try the second class
    try:
        store_link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"a.{class_name_2.replace(' ', '.')}"))
        )
        store_url = store_link_element.get_attribute("href")
        if store_url:
            print(f"Navigating to: {store_url}")
            driver.get(store_url)  # Navigate to the store URL
            return store_url
        else:
            print("No valid URL found in both attempts.")
            return None
    except Exception as e:
        print(f"Error finding the store link in the second class: {e}")
        return None


def close_login_window(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )
        close_button = driver.find_element(By.XPATH, "//div[@role='dialog']//div[@aria-label='Close']")
        close_button.click()
    except Exception as e:
        print("No login window detected or unable to close it.")

def extract_and_print_link(driver):
    try:
        # Wait until the page is fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        # Find all anchor tags
        link_elements = driver.find_elements(By.TAG_NAME, "a")

        # Iterate through the links and check if "reviews" is in the href
        for link in link_elements:
            href = link.get_attribute('href')
            if href and 'reviews' in href:
                print(f"Extracted Reviews Link: {href}")
                st.write(f"Reviews Link: {href}")  # Display the link in Streamlit
                return href  # Return the found reviews link

        print("No reviews link found.")

    except Exception as e:
        print(f"Error during extraction and printing: {e}")

def remove_comments_between_reviews(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    seen_reviews = set()
    skip_lines = False

    for line in lines:
        cleaned_line = line.strip()

        # Skip lines with a single character or that are empty
        if len(cleaned_line) <= 1:
            continue

        if "recommends" in cleaned_line or "doesn't recommend" in cleaned_line:
            skip_lines = False  # Stop skipping when a review starts
            if cleaned_line not in seen_reviews:
                cleaned_lines.append(cleaned_line)
                seen_reviews.add(cleaned_line)
        elif "comment" in cleaned_line:
            skip_lines = True  # Start skipping until the next review
        elif "All reactions:" in cleaned_line:
            continue  # Skip lines containing "All reactions:"
        elif not skip_lines:
            if cleaned_line not in seen_reviews:
                cleaned_lines.append(cleaned_line)
                seen_reviews.add(cleaned_line)  # Track seen reviews

    # Save cleaned reviews to a new file
    cleaned_file_name = 'reviews_after_cleaning.txt'
    with open(cleaned_file_name, 'w', encoding='utf-8') as file:
        for line in cleaned_lines:
            file.write(line + '\n')

    print(f"Comments removed, duplicates eliminated, and cleaned reviews saved to {cleaned_file_name}")

def check_and_close_login_window(driver):
    """
    Check if the Facebook login window appears and close it if found.
    Retry a few times if needed since the window might reappear.
    """
    retry_count = 0
    max_retries = 3  # You can adjust the number of retries if the window reappears
    
    while retry_count < max_retries:
        try:
            # Wait up to 5 seconds for the login window to appear
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            close_button = driver.find_element(By.XPATH, "//div[@role='dialog']//div[@aria-label='Close']")
            close_button.click()
            print("Login window detected and closed.")
            retry_count += 1  # Increment retry count if login dialog appears and is closed
        except Exception:
            print("No login window detected on this attempt.")
            break  # Exit the loop if no login window is detected
        time.sleep(2)  # Add a small delay before the next retry in case the login window reappears

    if retry_count >= max_retries:
        print("Login window appeared multiple times, tried closing it.")


def load_reviews(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    recommends = []
    does_not_recommend = []

    current_review = ""
    is_recommendation = False  # Flag to track if the current review is a recommendation

    for line in lines:
        line = line.strip()
        
        if "recommends" in line:
            if current_review:
                # Save the previous review to the correct list based on the flag
                if is_recommendation:
                    recommends.append(current_review.strip())
                else:
                    does_not_recommend.append(current_review.strip())
                
            current_review = line  # Start a new review
            is_recommendation = True  # Set flag to True for recommendation
            
        elif "doesn't recommend" in line:
            if current_review:
                # Save the previous review to the correct list based on the flag
                if is_recommendation:
                    recommends.append(current_review.strip())
                else:
                    does_not_recommend.append(current_review.strip())
                    
            current_review = line  # Start a new review
            is_recommendation = False  # Set flag to False for non-recommendation
            
        elif current_review:
            current_review += " " + line  # Continue the current review

    # Final check to add the last review
    if current_review:
        if is_recommendation:
            recommends.append(current_review.strip())
        else:
            does_not_recommend.append(current_review.strip())

    return recommends, does_not_recommend

def fetch_and_save_reviews(driver, url, before_cleaning_file):
    close_login_window(driver)

    time.sleep(5)
    driver.get(url)

    check_and_close_login_window(driver)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xdj266r')]"))
    )

    last_height = driver.execute_script("return document.body.scrollHeight")
    reviews_list = []
    review_count = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        check_and_close_login_window(driver)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or review_count >= 20:
            break
        last_height = new_height

        reviews = driver.find_elements(By.XPATH, "//div[contains(@class, 'xdj266r')]")
        for review in reviews:
            cleaned_review = review.text.strip()
            if (
                cleaned_review and 
                cleaned_review not in reviews_list and
                ("recommends" in cleaned_review or "doesn't recommend" in cleaned_review)
            ):
                reviews_list.append(cleaned_review)
                review_count += 1
                if review_count >= 20:
                    break

    print(f"Number of unique reviews found: {len(reviews_list)}")

    with open(before_cleaning_file, 'w', encoding='utf-8') as file:
        for review in reviews_list:
            file.write(review + '\n')

    print(f"Reviews before cleaning saved to {before_cleaning_file}")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Enable headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")

driver = None  # Initialize driver variable

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Your scraping code goes here

except Exception as e:
    print(f"An error occurred while initializing the driver: {e}")

finally:
    if driver is not None:  # Check if the driver was successfully created
        driver.quit()  # Ensure that driver is quit only if it was created

if st.button("Search"):
    if query:
        results = google_search(query, api_key, search_engine_id)

        # Display results and select one link
        if 'items' in results and len(results['items']) > 0:
            first_item = results['items'][0]  # Get the first link
            st.write(f"**Title:** {first_item['title']}")
            st.write(f"Link: {first_item['link']}")  # Print the raw link
            
            # Navigate to the initial link
            driver.get(first_item['link'])

            # Close any login dialog
            close_login_window(driver)  

            # Navigate to the main Facebook page
            main_page_url = navigate_to_facebook_main_page(driver)

            if main_page_url:
                # Call the extraction function and get the reviews link
                reviews_link = extract_and_print_link(driver)

                if reviews_link:
                    before_cleaning_file = 'reviews_before_cleaning.txt'
                    fetch_and_save_reviews(driver, reviews_link, before_cleaning_file)
                    driver.quit()

                    remove_comments_between_reviews(before_cleaning_file)
                    file_name = 'reviews_after_cleaning.txt'
                    recommends, does_not_recommend = load_reviews(file_name)

                    st.title("Reviews")

                    if recommends or does_not_recommend:
                        st.subheader("Recommendations")
                        if recommends:
                            for review in recommends:
                                st.write(f"- {review}")
                        else:
                            st.write("No recommendations found.")

                        st.subheader("Doesn't Recommend")
                        if does_not_recommend:
                            for review in does_not_recommend:
                                st.write(f"- {review}")
                        else:
                            st.write("No 'Doesn't Recommend' reviews found.")
                    else:
                        st.write("No reviews found.")
                else:
                    st.write("No reviews found.")
            else:
                st.write("Main Facebook page link not found.")
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a search query.")

driver.quit()
