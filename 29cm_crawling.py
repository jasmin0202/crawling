import nest_asyncio
import asyncio
from playwright.async_api import async_playwright

nest_asyncio.apply()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://shop.29cm.co.kr/best-items?category_large_code=268100100")
        await page.wait_for_timeout(3000)

        # 무한 스크롤
        for _ in range(3):
            await page.mouse.wheel(0, 2000)
            await page.wait_for_timeout(1000)

        # 상품 카드 가져오기
        cards = await page.query_selector_all('li[class^="css-1uzwmyc e1it8fm00"]')

        print(f"총 {len(cards)}개의 상품이 감지되었습니다.")

        for card in cards[:20]:
            # 이미지
            img_tag = await card.query_selector("img")
            img = await img_tag.get_attribute("src") if img_tag else "없음"

            # 링크
            link_tag = await card.query_selector("a")
            link = await link_tag.get_attribute("href") if link_tag else "없음"

            # 브랜드
            brand_tag = await card.query_selector("a:nth-of-type(1)")
            brand = await brand_tag.inner_text() if brand_tag else "없음"

            # 상품명
            name_tag = await card.query_selector("h5")
            name = await name_tag.inner_text() if name_tag else "없음"

            # 정가
            origin_tag = await card.query_selector("strong")
            origin_price = await origin_tag.inner_text() if origin_tag else "없음"

            # 판매가
            sale_tag = await card.query_selector("strong[class*='css-120pfho']")
            sale_price = await sale_tag.inner_text() if sale_tag else origin_price

            # 할인율
            discount_tag = await card.query_selector("span[class*='css-1nr17il']")
            discount = await discount_tag.inner_text() if discount_tag else "없음"
            
            # 좋아요 수
            like_tag = await  card.query_selector("button[class*='css-j1ov45']")
            like = await like_tag.inner_text() if like_tag else "0"

            # 리뷰 수
            review_tag = await card.query_selector("a[href*='#review'] span.review")
            review = await review_tag.inner_text() if review_tag else "없음"

            print(f"\n🛍️ {brand} | {name}")
            print(f"   링크: {link}")
            print(f"   이미지: {img}")
            print(f"   가격: {sale_price} (정가: {origin_price}, 할인율: {discount})")
            print(f"   좋아요 수: {like}")
            print(f"   리뷰 수: {review}")

        await browser.close()

asyncio.run(main())
