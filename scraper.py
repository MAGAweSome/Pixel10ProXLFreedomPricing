from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
import discord

load_dotenv()

# --- Discord Configuration ---
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

async def get_last_message():
    """Fetches the last message from the specified Discord channel."""
    if not DISCORD_CHANNEL_ID:
        print("DISCORD_CHANNEL_ID not found in .env file.")
        return None
    try:
        channel = await client.fetch_channel(int(DISCORD_CHANNEL_ID))
        async for message in channel.history(limit=1):
            return message.content
    except discord.errors.Forbidden:
        print("The bot does not have the necessary permissions to read the message history of the channel. Please make sure the bot has the 'Read Message History' permission.")
        return None
    except Exception as e:
        print(f"Could not fetch last message from Discord: {e}")
        return None

async def send_to_discord(message):
    """Sends a message to a Discord channel using the bot."""
    if not DISCORD_CHANNEL_ID:
        print("DISCORD_CHANNEL_ID not found in .env file.")
        return
    try:
        channel = await client.fetch_channel(int(DISCORD_CHANNEL_ID))
        await channel.send(message)
    except Exception as e:
        print(f"Could not send message to Discord: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    last_message = await get_last_message()

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

        # --- Retail Price ---
        retail_price_element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "$")]')))
        retail_price = retail_price_element.text
        
        # --- TradeUp Information ---
        tradeup_info = ""
        try:
            # Find the container for the TradeUp information using a CSS selector
            tradeup_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='tradeupAccordion']")))

            # Get the page source of the container
            page_source = tradeup_container.get_attribute('outerHTML')
            soup = BeautifulSoup(page_source, 'html.parser')

            # Retail Price
            retail_price_element = soup.find('span', attrs={'data-testid': 'msrp-value-trade-up'})
            tradeup_retail_price = retail_price_element.text.strip() if retail_price_element else "Not found"

            # Upfront Cost
            upfront_cost_element = soup.find('span', attrs={'data-testid': 'upfront-value-trade-up'})
            tradeup_upfront_cost = upfront_cost_element.text.strip() if upfront_cost_element else "Not found"

            # Savings
            savings_element = soup.find('span', attrs={'data-testid': 'phone-savings-value-trade-up'})
            tradeup_savings = savings_element.text.strip() if savings_element else "Not found"

            # TradeUp Amount
            tradeup_amount_element = soup.find('span', attrs={'data-testid': 'remaining-value-trade-up'})
            tradeup_amount = tradeup_amount_element.text.strip() if tradeup_amount_element else "Not found"

            # MyTab Savings
            mytab_savings_element = soup.find('span', attrs={'data-testid': 'mytab-savings-value'})
            tradeup_mytab_savings = mytab_savings_element.text.strip() if mytab_savings_element else "Not found"

            # Total MyTab Charge
            total_mytab_charge_element = soup.find('span', attrs={'data-testid': 'mytab-total-value'})
            tradeup_total_mytab_charge = total_mytab_charge_element.text.strip() if total_mytab_charge_element else "Not found"
            
            # Calculate Monthly Cost
            tradeup_monthly_cost = "Not found"
            if tradeup_total_mytab_charge != "Not found":
                try:
                    tradeup_monthly_cost = f"${float(tradeup_total_mytab_charge.replace(' ','').replace('$','')) / 24:.2f}/month"
                except (ValueError, ZeroDivisionError):
                    tradeup_monthly_cost = "Not found"

            # Required Plan
            required_plan_element = soup.find('div', attrs={'data-testid': 'return-policy-trade-up'})
            tradeup_required_plan = required_plan_element.text.strip() if required_plan_element else "Not found"

            tradeup_info = f"""**TradeUp Information:** {tradeup_monthly_cost}
Retail Price: {tradeup_retail_price}
Upfront Cost: {tradeup_upfront_cost}
Savings: {tradeup_savings}
TradeUp Amount: {tradeup_amount}
MyTab Savings: {tradeup_mytab_savings}
Total MyTab Charge: {tradeup_total_mytab_charge}
Required Plan: {tradeup_required_plan}
"""

        except Exception as e:
            tradeup_info = f"Could not retrieve TradeUp information: {e}"

        # --- MyTab Information ---
        mytab_info = ""
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
            mytab_retail_price = retail_price_element.text.strip() if retail_price_element else "Not found"

            # Upfront Cost
            upfront_cost_element = soup.find('span', attrs={'data-testid': 'upfront-value-mytab'})
            mytab_upfront_cost = upfront_cost_element.text.strip() if upfront_cost_element else "Not found"

            # MyTab Savings
            mytab_savings_element = soup.find('span', attrs={'data-testid': 'phone-savings-value-mytab'})
            mytab_savings = mytab_savings_element.text.strip() if mytab_savings_element else "Not found"

            # Total MyTab Charge
            total_mytab_charge_element = soup.find('span', attrs={'data-testid': 'mytab-total-value'})
            mytab_total_mytab_charge = total_mytab_charge_element.text.strip() if total_mytab_charge_element else "Not found"

            # Calculate Monthly Cost
            mytab_monthly_cost = "Not found"
            if mytab_total_mytab_charge != "Not found":
                try:
                    mytab_monthly_cost = f"${float(mytab_total_mytab_charge.replace(' ','').replace('$','')) / 24:.2f}/month"
                except (ValueError, ZeroDivisionError):
                    mytab_monthly_cost = "Not found"

            # Required Plan
            required_plan_element = soup.find('div', attrs={'data-testid': 'return-policy-mytab'})
            mytab_required_plan = required_plan_element.text.strip() if required_plan_element else "Not found"

            mytab_info = f"""**MyTab Information:** {mytab_monthly_cost}
Retail Price: {mytab_retail_price}
Upfront Cost: {mytab_upfront_cost}
MyTab Savings: {mytab_savings}
Total MyTab Charge: {mytab_total_mytab_charge}
Required Plan: {mytab_required_plan}
"""

        except Exception as e:
            mytab_info = f"Could not retrieve MyTab information: {e}"

        # --- Send to Discord ---
        message = f"""**Freedom Mobile Pixel 10 Pro XL Pricing:**

{tradeup_info}
{mytab_info}
"""
        
        if message != last_message:
            await send_to_discord(message)
            print(message)
        else:
            print("Pricing has not changed. No message sent to Discord.")

    except Exception as e:
        error_message = f"An error occurred: {e}"
        await send_to_discord(error_message)
        print(error_message)

    finally:
        # Close the browser
        driver.quit()
        await client.close()

if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN or not DISCORD_CHANNEL_ID:
        print("DISCORD_BOT_TOKEN or DISCORD_CHANNEL_ID not found in .env file.")
    else:
        try:
            client.run(DISCORD_BOT_TOKEN)
        except discord.errors.LoginFailure:
            print("Improper token has been passed. Please make sure you have the correct bot token in your .env file.")
