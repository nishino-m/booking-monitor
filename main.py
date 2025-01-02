from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests

def main():
    LINE_TOKEN = "xxx"
    ENDPOINT = "https://notify-api.line.me/api/notify"
    TARGET_WEB_URL = "https://stairs.booking.chillnn.com"

    result=check_web_site(TARGET_WEB_URL)

    if result:
        if isinstance(result, str):
            send_line_notify(ENDPOINT,result,LINE_TOKEN)
        else:
            message = "予約に空きがありました"
            send_line_notify(ENDPOINT,message,LINE_TOKEN)

def send_line_notify(endpoint,message,token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}

    try:
        requests.post(endpoint, headers=headers, data=data)

    except requests.exceptions.RequestException as err:
        print(f"通信エラー: {err}")

def check_web_site(url):
    options=Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))

    try:
        driver.get(url)
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        el=driver.find_elements(By.CLASS_NAME,'text-center')
        for element in el:
            if '◯' in element.text or '⚪︎' in element.text:
                return True
            
        return False
    
    except Exception as err:
        return "システムエラーが発生しました。確認してください"
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
