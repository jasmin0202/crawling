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

base_url = "https://www.generalidea.co.kr"
start_url = base_url + "/product/list.html?cate_no=353&sort_method=5#Product_ListMenu"
driver.get(start_url)
time.sleep(2)

page_count = 1
max_pages = 2

while page_count <= max_pages:
    print(f"{page_count} 페이지 수집 중...")

    products = driver.find_elements(By.CSS_SELECTOR, "ul.prdList li[id^='anchorBoxId_']")

    product_infos = []

    for p in products:
        try:
            inner_html = p.get_attribute('innerHTML')
            soup = BeautifulSoup(inner_html, 'html.parser')

            img_tag = soup.select_one('.thumbnail .prdImg img.thumber_2') or soup.select_one('.thumbnail .prdImg img.thumber_1')
            img = img_tag['src'] if img_tag else '이미지 없음'

            name_tag = soup.select_one('.description .name a')
            name_raw = name_tag.text if name_tag else '상품명 없음'
            name = name_raw.split(':')[-1].strip()

            price_tag = soup.select_one('li.product_price span')
            price = price_tag.text if price_tag else '가격 없음'

            link_tag = soup.select_one('div.prdImg a')
            relative_link = link_tag['href'] if link_tag else ''
            link = base_url + relative_link

            product_infos.append({
                'name': name,
                'price': price,
                'img': img,
                'link': link
            })

        except Exception as e:
            print("에러 발생 (리스트페이지):", e)
            continue

    for info in product_infos:
        try:
            driver.get(info['link'])
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            detail_imgs = driver.find_elements(By.CSS_SELECTOR, '#prdDetailContentLazy center img')
            if len(detail_imgs) >= 2:
                target_img = detail_imgs[-2]
            elif detail_imgs:
                target_img = detail_imgs[-1]
            else:
                target_img = None

            if target_img:
                detail_img_src = target_img.get_attribute('src')

                if detail_img_src.startswith("data:image"):
                    # base64면 data-original 시도
                    detail_img_original = target_img.get_attribute('data-original') or target_img.get_attribute('data-src')
                    if detail_img_original:
                        detail_img = detail_img_original
                    else:
                        detail_img = "상세 이미지 로딩 실패 (base64)"
                else:
                    detail_img = detail_img_src
            else:
                detail_img = "상세 이미지 없음"

            print(f"상품명: {info['name']} | 가격: {info['price']} | 썸네일: {info['img']} | 상세이미지: {detail_img}")

        except Exception as e:
            print("에러 발생 (상세페이지):", e)
            continue

    try:
        next_buttons = driver.find_elements(By.CSS_SELECTOR, 'a.first_nt')
        if len(next_buttons) >= 2:
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
