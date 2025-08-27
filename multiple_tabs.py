import time
from selenium import webdriver
import threading

def run_bot():
    user_agent = """Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"""
    browser_language = "de"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument(f"--lang={browser_language}")
    options.add_argument("--headless")
    bot = webdriver.Chrome(options=options)
    # bot.minimize_window()
    bot.get_cookies()
    bot.delete_all_cookies()


    for i in range(0,1):
        bot.get_cookies()
        bot.delete_all_cookies()
        # bot.minimize_window()
        bot.get("https://plio.ovrinta.com/?mid=258665_1588577")
        try:
            affiliate_data = bot.execute_script("return window.localStorage.getItem('AFFILIATE');")
            print(f"[Thread-{threading.get_ident()}] AFFILIATE localStorage: {affiliate_data}")
        except Exception as e:
            print(f"[Thread-{threading.get_ident()}] Failed to read localStorage: {e}")
        bot.switch_to.window(bot.window_handles[-1])
        time.sleep(1)
    time.sleep(1)

if __name__ == "__main__":
    threads = []
    for _ in range(0, 20):
        t = threading.Thread(target=run_bot)
        time.sleep(1)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
        time.sleep(1)
