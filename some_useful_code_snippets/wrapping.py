import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with the path to your ChromeDriver
chrome_driver_path = '/Users/huseyin/Downloads/chromedriver-mac-x64/chromedriver'

# Read firm codes from the file
with open('/Users/huseyin/Downloads/only_firms_code_unique.txt', 'r') as file:
    firm_codes = file.read().splitlines()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("prefs", {
    "download.prompt_for_download": False,
    "download.default_directory": "/Users/huseyin/Downloads",  # Change to your download directory
    "directory_upgrade": True
})

# Start WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

# Open the login page and wait for manual login
login_url = 'https://fintables.com/auth/login'
driver.get(login_url)

# Wait for manual login
input("Please log in manually and then press Enter here to continue...")

# Iterate over each firm code and download the Excel file
base_url = 'https://fintables.com/sirketler/{firm}/finansal-tablolar/bilanco'

for firm in firm_codes:
    firm_url = base_url.format(firm=firm)
    driver.get(firm_url)
    try:
        excel_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), \"Excel'e Aktar\")]")))
        excel_button.click()
        time.sleep(5)  # Wait for the download to complete
        print(f"Downloaded Excel for {firm}")
    except Exception as e:
        print(f"Failed to download for {firm}: {e}")

# Close the WebDriver
driver.quit()
