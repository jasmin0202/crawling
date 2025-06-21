from libs.accounts import accounts
from instagram_crawler import scroll_and_collect_images

import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# 환경 변수 불러오기
load_dotenv()
INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")
INSTAGRAM_PW = os.getenv("INSTAGRAM_PW")

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
driver_path = os.path.join(BASE_DIR, "chrome", "chromedriver")

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# 드라이버 실행
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 자동화 감지 방지
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    },
)

# 인스타그램 로그인 페이지 이동
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

# 로그인 요소 선택 (직접 DOM 경로 지정)
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(2)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver.get("https://www.instagram.com/accounts/login/")
time.sleep(2)

try:
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_input.send_keys(INSTAGRAM_ID)
    password_input.send_keys(INSTAGRAM_PW)
    login_button.click()
    time.sleep(5)

except Exception as e:
    with open("login_page_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("❌ 로그인 중 오류:", e)

driver.get("https://www.instagram.com/")
time.sleep(5)

for account in accounts:
    urls = scroll_and_collect_images(driver, account, max_scroll=4)
    print(f"\ [{account}] 총 {len(urls)}개 이미지 수집 완료")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")

input("\n✔️ 크롬 종료하려면 엔터를 누르세요.")
driver.quit()