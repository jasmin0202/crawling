from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

# 셀레니움 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_url = "https://slowand.com"
start_url = base_url + "/product/list.html?cate_no=66"
driver.get(start_url)
time.sleep(2)

page_count = 1
max_pages = 2

while page_count <= max_pages:
    print(f"{page_count} 페이지 수집 중...")

    products = driver.find_elements(By.CSS_SELECTOR, "ul.prdList li[id^='anchorBoxId_']")

    for p in products:
        try:
            inner_html = p.get_attribute('innerHTML')
            soup = BeautifulSoup(inner_html, 'html.parser')

            # 이미지
            img_tag = soup.select_one('.prdImg img')
            img = img_tag['src'] if img_tag else '이미지 없음'
            img = "https:" + img if img.startswith("//") else img

            # 상품명
            name_tag = soup.select_one('.description .name a')
            name = name_tag.text.strip() if name_tag else '상품명 없음'

            # 판매가
            price_spans = soup.select('.priceLine li.listPrice span')
            if len(price_spans) >= 2:
                price = price_spans[1].text.strip()
            else:
                price = '가격 없음'

            # 링크
            link_tag = soup.select_one('.prdImg a')
            relative_link = link_tag['href'] if link_tag else ''
            link = base_url + relative_link

            print(f"{name} | 가격: {price} | 썸네일: {img} | 링크: {link} \n")

        except Exception as e:
            print("에러 발생:", e)
            continue

    # 페이징 이동 more버튼 누르고 들어가야 해서 상품 개수가 좀 제한 (코드 수정/문의)
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')
        if next_button.is_enabled():
            next_button.click()
            time.sleep(3)
            page_count += 1
        else:
            print("다음 페이지 없음. 종료")
            break
    except:
        print("다음 페이지 없음. 종료")
        break

driver.quit()
print("모든 페이지 크롤링 완료!")
