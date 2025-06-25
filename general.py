from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# 셀레니움 브라우저 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 시작 URL
base_url = "https://www.generalidea.co.kr"
start_url = base_url + "/product/list.html?cate_no=353&sort_method=5#Product_ListMenu"
driver.get(start_url)
time.sleep(3)

page_count = 1
max_pages = 2

while page_count <= max_pages:
    print(f"{page_count} 페이지 수집 중...")

    products = driver.find_elements(By.CSS_SELECTOR, "ul.prdList li[id^='anchorBoxId_']")

    for p in products:
        try:
            inner_html = p.get_attribute('innerHTML')
            soup = BeautifulSoup(inner_html, 'html.parser')

            # 이미지 (thumber_2 우선, 없으면 thumber_1)
            img_tag = soup.select_one('.thumbnail .prdImg img.thumber_2') or soup.select_one('.thumbnail .prdImg img.thumber_1')
            img = img_tag['src'] if img_tag else '이미지 없음'

            # 상품명
            name_tag = soup.select_one('.description .name a')
            if name_tag:
                name_raw = name_tag.text
                name = name_raw.split(':')[-1].strip()
            else:
                name = '상품명 없음'

            # li 전체 긁기
            price_li = soup.select_one('li.product_price')
            if price_li:
                # 전체 문자열 가져오기 (공백 포함)
                full_text = price_li.get_text(separator=' ', strip=True)
                
                # ₩ 포함된 부분만 찾아서 추출
                price_candidates = [part for part in full_text.split() if '₩' in part]
                
                if price_candidates:
                    price = price_candidates[0]  # 첫번째 ₩ 가격 추출
                else:
                    price = '가격 없음'
            else:
                price = '가격 없음'




            # 링크
            link_tag = soup.select_one('div.prdImg a')
            relative_link = link_tag['href'] if link_tag else ''
            link = base_url + relative_link

            print(f"상품명: {name} | 가격: {price} | 링크: {link} | 이미지: {img} \n")

        except Exception as e:
            print("에러 발생:", e)
            continue

    # 다음 페이지 이동 (페이징 구조 확인)
    try:
        next_buttons = driver.find_elements(By.CSS_SELECTOR, 'a.first_nt')
        if len(next_buttons) >= 2:
            # 두 번째 first_nt가 오른쪽 화살표 (다음 페이지)
            next_buttons[1].click()
            time.sleep(3)
            page_count += 1
        else:
            print("다음 페이지 없음. 종료")
            break
    except Exception as e:
        print("페이지 이동 중 에러:", e)
        break


driver.quit()
print("모든 페이지 크롤링 완료!")

