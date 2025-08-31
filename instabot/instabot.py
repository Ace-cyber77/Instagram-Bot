import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

# === CONFIG ===
EMAIL = "ragnarokismac@gmail.com"
FULL_NAME = "ragnarok"
USERNAME_FILE = "user01.txt"
PASSWORD_FILE = "pass01.txt"
CHROMEDRIVER_PATH = r"D:\chromedriver\chromedriver-win64\chromedriver.exe"
DELAY_PER_CHAR = 0.25  # Typing delay per character
FINAL_DELAY = 5000  # Seconds to wait for manual code entry

# === Read user and pass from files ===
with open(USERNAME_FILE, "r") as uf, open(PASSWORD_FILE, "r") as pf:
    usernames = [line.strip() for line in uf if line.strip()]
    passwords = [line.strip() for line in pf if line.strip()]

if len(usernames) == 0 or len(passwords) == 0 or len(usernames) != len(passwords):
    print("❌ Error: Username and password counts do not match or are empty.")
    exit()

username = usernames[0]
password = passwords[0]

# === Setup Chrome ===
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# === Simulate typing URL with delay ===
url = "https://www.instagram.com/accounts/emailsignup/"
print("⏳ Typing URL with delay...")
for char in url:
    print(char, end='', flush=True)
    time.sleep(DELAY_PER_CHAR)
driver.get(url)
time.sleep(2)

# === Utility function for typing with delay ===
def type_with_delay(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(DELAY_PER_CHAR)

# === Fill Email ===
email_box = driver.find_element(By.NAME, "emailOrPhone")
type_with_delay(email_box, EMAIL)
time.sleep(1)

# === Fill Full Name ===
full_name_box = driver.find_element(By.NAME, "fullName")
type_with_delay(full_name_box, FULL_NAME)
time.sleep(1)

# === Fill Username ===
username_box = driver.find_element(By.NAME, "username")
print("⏳ Typing username...")
type_with_delay(username_box, username)
time.sleep(1)

# === Fill Password ===
password_box = driver.find_element(By.NAME, "password")
print("⏳ Typing password...")
type_with_delay(password_box, password)
time.sleep(1)

# === Click Sign Up button ===
submit_btn = driver.find_element(By.XPATH, '//button[@type="submit"]')
submit_btn.click()
time.sleep(3)

# === Fill DOB ===
try:
    # Wait for DOB page
    time.sleep(5)

    # Random DOB values
    random_month = random.randint(1, 12)
    random_day = random.randint(1, 28)
    random_year = random.randint(1985, 2003)

    # Month
    month_dropdown = Select(driver.find_element(By.XPATH, "//select[@title='Month:']"))
    month_dropdown.select_by_index(random_month)
    time.sleep(5)

    # Day
    day_dropdown = Select(driver.find_element(By.XPATH, "//select[@title='Day:']"))
    day_dropdown.select_by_visible_text(str(random_day))
    time.sleep(5)

    # Year
    year_dropdown = Select(driver.find_element(By.XPATH, "//select[@title='Year:']"))
    year_dropdown.select_by_visible_text(str(random_year))
    time.sleep(5)

    # Click Next
    next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
    next_btn.click()
except NoSuchElementException:
    print("⚠️ DOB page not found or skipped.")

# === Click until confirmation code screen ===
while True:
    try:
        # Break loop if confirmation input box appears
        driver.find_element(By.NAME, "email_confirmation_code")
        print("✅ Confirmation screen reached.")
        break
    except NoSuchElementException:
        try:
            next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
            next_btn.click()
            time.sleep(2)
        except NoSuchElementException:
            break

# === Final Wait ===
print(f"⏸ Waiting {FINAL_DELAY} seconds for manual verification...")
time.sleep(FINAL_DELAY)

driver.quit()
