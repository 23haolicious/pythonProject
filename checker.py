import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchFrameException
from datetime import datetime
import requests

# === CONFIG ===
URLS = [
    "https://plio.ovrinta.com/?mid=280122_1645999",
    "https://plio.ovrinta.com/?mid=245715_1664056",
    "https://plio.ovrinta.com/?mid=258665_1584446",
]
SEARCH_TERMS = ["247022"]
WAIT_SECONDS = 5
LOG_FILE = "iframe_scan_log.txt"

# === TELEGRAM (optional) ===
TELEGRAM_ENABLED = False
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"

def send_telegram(message):
    if TELEGRAM_ENABLED:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

# === CHROME SETUP ===
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=375,812")
options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1")

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    print(full_message)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_message + "\n")

def contains_search_term(text):
    for term in SEARCH_TERMS:
        if term in text:
            return term
    return None

def run_scan():
    browser = webdriver.Chrome(options=options)

    for url in URLS:
        log(f"🌐 Visiting {url}")
        browser.get(url)
        time.sleep(WAIT_SECONDS)

        iframes = browser.find_elements(By.TAG_NAME, "iframe")
        log(f"🔎 Found {len(iframes)} iframe(s)")

        for i, iframe in enumerate(iframes, start=1):
            src = iframe.get_attribute("src") or "[empty]"
            outer = iframe.get_attribute("outerHTML").strip()
            log(f"🖼️ iframe #{i} src: {src}")
            log(f"↪️ outerHTML: {outer[:300]}...")

            try:
                browser.switch_to.frame(iframe)
                time.sleep(1)
                doc = browser.page_source.strip().replace("\n", "")
                snippet = doc[:1000]
                log(f"📄 #document (first 1000 chars): {snippet}")

                match = contains_search_term(doc)
                if match:
                    alert = f"❗ MATCH FOUND in iframe #{i} ({url}): '{match}'"
                    log(alert)
                    send_telegram(alert)

                browser.switch_to.default_content()
            except (NoSuchFrameException, WebDriverException) as e:
                log(f"⚠️ iframe #{i} could not be read: {e}")
                browser.switch_to.default_content()

    browser.quit()
    log("✅ Scan complete.")

# === Run this once, or call it on a schedule ===
if __name__ == "__main__":
    run_scan()
