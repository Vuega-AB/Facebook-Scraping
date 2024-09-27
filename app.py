import requests
import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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
api_key = 'AIzaSyAcEhygRJDoBeCBePgPxTxlwWGSXmnGTwo'  # Replace with your API key
search_engine_id = '70fd339e45a0e4b2c'  # Replace with your Search Engine ID

# Streamlit app layout
st.title("Google Custom Search")
query = st.text_input("Enter your search query:")

def navigate_to_facebook_main_page(driver):
    class_name_1 = "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5qnf xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1sur9pj xkrqix3 xzsf02u x1s688f"
    class_name_2 = "x1i10hfl xe8uvvx xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz xjyslct xjbqb8w x18o3ruo x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g x1ypdohk xdj266r x11i5qnf xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg x1vjfegm x3nfvp2 xrbpyxo x1itg65n x16dsc37"

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
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        link_elements = driver.find_elements(By.TAG_NAME, "a")

        for link in link_elements:
            href = link.get_attribute('href')
            if href and 'reviews' in href:
                print(f"Extracted Reviews Link: {href}")
                st.write(f"Reviews Link: {href}")  # Display the link in Streamlit
                return href

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

        if len(cleaned_line) <= 1:
            continue

        if "recommends" in cleaned_line or "doesn't recommend" in cleaned_line:
            skip_lines = False
            if cleaned_line not in seen_reviews:
                cleaned_lines.append(cleaned_line)
                seen_reviews.add(cleaned_line)
        elif "comment" in cleaned_line:
            skip_lines = True
        elif "All reactions:" in cleaned_line:
            continue
        elif not skip_lines:
            if cleaned_line not in seen_reviews:
                cleaned_lines.append(cleaned_line)
                seen_reviews.add(cleaned_line)

    cleaned_file_name = 'reviews_after_cleaning.txt'
    with open(cleaned_file_name, 'w', encoding='utf-8') as file:
        for line in cleaned_lines:
            file.write(line + '\n')

    print(f"Comments removed, duplicates eliminated, and cleaned reviews saved to {cleaned_file_name}")

def check_and_close_login_window(driver):
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
            close_button = driver.find_element(By.XPATH, "//div[@role='dialog']//div[@aria-label='Close']")
            close_button.click()
            print("Login window detected and closed.")
            retry_count += 1
        except Exception:
            print("No login window detected on this attempt.")
            break
        time.sleep(2)

    if retry_count >= max_retries:
        print("Login window appeared multiple times, tried closing it.")

def load_reviews(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    recommends = []
    does_not_recommend = []

    current_review = ""
    is_recommendation = False

    for line in lines:
        line = line.strip()
        
        if "recommends" in line:
            if current_review:
                if is_recommendation:
                    recommends.append(current_review.strip())
                else:
                    does_not_recommend.append(current_review.strip())
                
            current_review = line
            is_recommendation = True
            
        elif "doesn't recommend" in line:
            if current_review:
                if is_recommendation:
                    recommends.append(current_review.strip())
                else:
                    does_not_recommend.append(current_review.strip())
                    
            current_review = line
            is_recommendation = False
            
        elif current_review:
            current_review += " " + line

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
            try:
                review_text = review.text
                if review_text and review_text not in reviews_list:
                    reviews_list.append(review_text)
                    review_count += 1
            except Exception as e:
                print(f"Error extracting review: {e}")

    with open(before_cleaning_file, 'w', encoding='utf-8') as f:
        for review in reviews_list:
            f.write(review + "\n")
            
    print(f"Reviews extracted and saved to {before_cleaning_file}")

# Main app logic
if st.button("Search and Extract Reviews"):
    if query:
        search_result = google_search(query, api_key, search_engine_id)
        items = search_result.get("items", [])
        
        if items:
            st.subheader("Search Results")
            for i, item in enumerate(items):
                st.write(f"{i + 1}. {item['title']} - [Link]({item['link']})")

            st.write("Navigating to Facebook page for reviews...")

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(items[0]['link'])  # Use the first search result

            store_url = navigate_to_facebook_main_page(driver)
            if store_url:
                reviews_link = extract_and_print_link(driver)
                if reviews_link:
                    before_cleaning_file = 'reviews_before_cleaning.txt'
                    fetch_and_save_reviews(driver, reviews_link, before_cleaning_file)

                    # Load reviews from the file and display
                    recommends, does_not_recommend = load_reviews(before_cleaning_file)
                    
                    st.write("### Recommendations")
                    for rec in recommends:
                        st.write(f"- {rec}")

                    st.write("### Doesn't Recommend")
                    for rec in does_not_recommend:
                        st.write(f"- {rec}")

            driver.quit()
        else:
            st.write("No results found.")
    else:
        st.write("Please enter a query.")
