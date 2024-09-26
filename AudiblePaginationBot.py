from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# URL and ChromeDriver path
web = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=adc4b13b-d074-4e1c-ac46-9f54aa53072b&pf_rd_r=1F7DV0MPHV77Z61RX566"
path = r'C:\Users\KIIT\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Correct your path here

# Initialize driver
driver = webdriver.Chrome(executable_path=path)
driver.get(web)
driver.maximize_window()

# Locate pagination
pagination = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "pagingElements")]'))
)
pages = pagination.find_elements(By.TAG_NAME, 'li')
last_page = int(pages[-2].text)  # Second last element contains the last page number

# Lists to store data
book_title = []
book_author = []
book_length = []
current_page = 1

# Scraping loop
while current_page <= last_page:
    # Implicit wait to allow content to load
    time.sleep(2)
    
    # Explicit wait to ensure the container is present
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container'))
    )
    
    # Explicit wait to ensure all products are loaded in the container
    products = WebDriverWait(container, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class, "productListItem")]'))
    )

    # Extracting data for each product
    for product in products:
        book_title.append(product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text)

    current_page += 1  # Move to the next page

    # Try clicking the 'Next' button
    try:
        next_page = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, './/span[contains(@class, "nextButton")]'))
        )
        next_page.click()  # Go to the next page
    except Exception as e:
        print(f"Could not navigate to the next page: {e}")
        break

# Quit the driver after scraping is complete
driver.quit()

# Create DataFrame and save to CSV
df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books_pagination.csv', index=False)

print("Scraping complete. Data saved to 'books_pagination.csv'")
