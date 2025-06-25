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

base_url = "https://reetkeem.com"
start_url = base_url + "/category/best/69/"
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
            img_tag = soup.select_one('.thumbnail img')
            img = img_tag['src'] if img_tag else '이미지 없음'
            img = "https:" + img if img.startswith("//") else img

            # 상품명
            name_tag = soup.select_one('.description .name a')
            name = name_tag.text.strip() if name_tag else '상품명 없음'

            # 판매가
            price_li = soup.select_one('ul.xans-product-listitem li.xans-record-')
            if price_li:
                spans = price_li.find_all('span')
                if len(spans) >= 2:
                    price = spans[1].text.strip()
                else:
                    price = '가격 없음'
            else:
                price = '가격 없음'


            # 링크
            link_tag = soup.select_one('div.thumbnail a')
            if link_tag:
                relative_link = link_tag['href']
                link = base_url + relative_link
            else:
                link = '링크 없음'
 # 컬러칩
            color_spans = soup.select('.description .color span.chips')
            colors = [span['title'] for span in color_spans if 'title' in span.attrs]
            color_str = ', '.join(colors) if colors else '컬러 없음'

            # 결과 출력
            print(f"{name} | 가격: {price} | 썸네일: {img} | 링크: {link} | 컬러: {color_str}")


        except Exception as e:
            print("에러 발생:", e)
            continue

    # 페이징 이동 (이 사이트도 버튼이 좀 다름)
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, '#contents > div > div.xans-element-.xans-product.xans-product-normalpaging.ec-base-paginate.angle > a:nth-child(4) > span > i')
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