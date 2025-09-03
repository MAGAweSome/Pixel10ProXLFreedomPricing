from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Setup Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the product page
url = "https://shop.freedommobile.ca/en-CA/devices/Google/Pixel-10-Pro-XL"

try:
    # Open the URL
    driver.get(url)

    # Wait for the page to load
    wait = WebDriverWait(driver, 20) # Increased wait time

    # --- TradeUp Information ---
    print("\n--- TradeUp Information ---")
    try:
        # Find the container for the TradeUp information using a CSS selector
        tradeup_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='tradeupAccordion']")))

        # Get the page source of the container
        page_source = tradeup_container.get_attribute('outerHTML')
        soup = BeautifulSoup(page_source, 'html.parser')

        # Retail Price
        retail_price_element = soup.find('span', attrs={'data-testid': 'msrp-value-trade-up'})
        retail_price = retail_price_element.text.strip() if retail_price_element else "Not found"
        print(f"Retail Price: {retail_price}")

        # Upfront Cost
        upfront_cost_element = soup.find('span', attrs={'data-testid': 'upfront-value-trade-up'})
        upfront_cost = upfront_cost_element.text.strip() if upfront_cost_element else "Not found"
        print(f"Upfront Cost: {upfront_cost}")

        # Savings
        savings_element = soup.find('span', attrs={'data-testid': 'phone-savings-value-trade-up'})
        savings = savings_element.text.strip() if savings_element else "Not found"
        print(f"Savings: {savings}")

        # TradeUp Amount
        tradeup_amount_element = soup.find('span', attrs={'data-testid': 'remaining-value-trade-up'})
        tradeup_amount = tradeup_amount_element.text.strip() if tradeup_amount_element else "Not found"
        print(f"TradeUp Amount: {tradeup_amount}")

        # MyTab Savings
        mytab_savings_element = soup.find('span', attrs={'data-testid': 'mytab-savings-value'})
        mytab_savings = mytab_savings_element.text.strip() if mytab_savings_element else "Not found"
        print(f"MyTab Savings: {mytab_savings}")

        # Total MyTab Charge
        total_mytab_charge_element = soup.find('span', attrs={'data-testid': 'mytab-total-value'})
        total_mytab_charge = total_mytab_charge_element.text.strip() if total_mytab_charge_element else "Not found"
        print(f"Total MyTab Charge: {total_mytab_charge}")

        # Required Plan
        required_plan_element = soup.find('div', attrs={'data-testid': 'return-policy-trade-up'})
        required_plan = required_plan_element.text.strip() if required_plan_element else "Not found"
        print(f"Required Plan: {required_plan}")

    except Exception as e:
        print(f"Could not retrieve TradeUp information: {e}")

    # --- MyTab Information ---
    print("\n--- MyTab Information ---")
    try:
        # Find and click the MyTab tab
        mytab_tab = driver.find_element(By.XPATH, '//div[contains(text(), "MyTab")]')
        # Scroll to the tab and click with JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", mytab_tab)
        driver.execute_script("arguments[0].click();", mytab_tab)
        
        # Find the container for the MyTab information using a CSS selector
        mytab_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='myTabAccordion']")))

        # Get the page source of the container
        page_source = mytab_container.get_attribute('outerHTML')
        soup = BeautifulSoup(page_source, 'html.parser')

        # Retail Price
        retail_price_element = soup.find('span', attrs={'data-testid': 'msrp-value-mytab'})
        retail_price = retail_price_element.text.strip() if retail_price_element else "Not found"
        print(f"Retail Price: {retail_price}")

        # Upfront Cost
        upfront_cost_element = soup.find('span', attrs={'data-testid': 'upfront-value-mytab'})
        upfront_cost = upfront_cost_element.text.strip() if upfront_cost_element else "Not found"
        print(f"Upfront Cost: {upfront_cost}")

        # MyTab Savings
        mytab_savings_element = soup.find('span', attrs={'data-testid': 'phone-savings-value-mytab'})
        mytab_savings = mytab_savings_element.text.strip() if mytab_savings_element else "Not found"
        print(f"MyTab Savings: {mytab_savings}")

        # Total MyTab Charge
        total_mytab_charge_element = soup.find('span', attrs={'data-testid': 'mytab-total-value'})
        total_mytab_charge = total_mytab_charge_element.text.strip() if total_mytab_charge_element else "Not found"
        print(f"Total MyTab Charge: {total_mytab_charge}")

        # Required Plan
        required_plan_element = soup.find('div', attrs={'data-testid': 'return-policy-mytab'})
        required_plan = required_plan_element.text.strip() if required_plan_element else "Not found"
        print(f"Required Plan: {required_plan}")

    except Exception as e:
        print(f"Could not retrieve MyTab information: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()