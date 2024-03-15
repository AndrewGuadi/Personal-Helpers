from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os
import json
from gpt_helpers import OpenAIHelper
# from run import test_extract_jobs

def write_json(data, file_path):
    """
    Write a large array or any data structure to a JSON file.

    Parameters:
    data (any): The data to be written to the file.
    file_path (str): The path of the file where the data will be saved.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")




def read_json(file_path):
    """
    Read a JSON file that contains an array of dictionaries. For each top-level dictionary,
    retain the sub-keys that have non-empty values.

    Parameters:
    file_path (str): The path of the JSON file to be read.

    Returns:
    list: A list of dictionaries with filtered sub-keys.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
  
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def init_webdriver():
    # Setup Selenium to use Chrome
    s = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')  # Set log level to avoid most logs except fatal errors
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


def take_screenshot(driver, url, path):
    try:
        # Go to the website
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Retrieve the dimensions of the entire page
        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")

        # Resize window to capture the whole page
        driver.set_window_size(total_width, total_height)

        # Additional wait for the resize action
        time.sleep(3)

        # Take a screenshot
        driver.save_screenshot(path)
        print("Screenshot Saved")

    except Exception as e:
        print(f"An error occurred: {e}")


def close_webdriver(driver):
    # Close the browser and end the session
    driver.quit()







if __name__ == "__main__":

    #get data from schoolLinks
    df = pd.read_csv(r'C:\Users\Gersh\CODEOS\teacherScraping\schoolLinks.csv')

    #get data from newJobs
    jobs_data = read_json(r'C:\Users\Gersh\CODEOS\teacherScraping\jsonData\newJobs.json')   
    
    proper_data = []

    for item in jobs_data:
        for url, jobs in item.items():
            # Search for the row where the Employment Page URL matches
            result = df[df['Employment Page URL'] == url]
            
            # Check if the result is not empty
            if not result.empty:
                # Extract the district name as a string
                district = result['School District'].values[0]

                data = {
                    'url': url,
                    'schoolDistrict': district,
                    'jobs':jobs
                }
                proper_data.append(data)
                
            else:
                print("No matching district found")

    write_json(proper_data, 'jsonData/formatted_jobs.json')