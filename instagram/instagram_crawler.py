import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scroll_and_collect_images(driver, account_name, max_scroll=4):
    url = f"https://www.instagram.com/{account_name}/"
    driver.get(url)
    time.sleep(3)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    except TimeoutException:
        print(f"❌ {account_name} - main 태그 로딩 실패")
        return set()

    print(f"\n [{account_name}] 무한 스크롤 시작...")
    img_urls = set()
    same_count = 0
    SCROLL_PAUSE_TIME = 2

    for i in range(max_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        img_tags = driver.find_elements(By.TAG_NAME, "img")
        prev_count = len(img_urls)

        for img in img_tags:
            try:
                src = img.get_attribute("src")
                alt = img.get_attribute("alt")
                if src and "scontent" in src and alt:
                    img_urls.add(src)
            except:
                continue

        now_count = len(img_urls)
        print(f"🔻 {i+1}회 스크롤 후 누적 이미지 수: {now_count}")

        if now_count == prev_count:
            same_count += 1
            if same_count >= 3:
                print(" 더 이상 새로운 이미지가 로드되지 않음. 스크롤 중단.")
                break
        else:
            same_count = 0

    return img_urls