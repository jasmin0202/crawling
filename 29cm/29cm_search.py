import nest_asyncio
import asyncio
from playwright.async_api import async_playwright

nest_asyncio.apply()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://shop.29cm.co.kr/search/start")
        await page.wait_for_timeout(2000)

        # 모든 랭킹 항목 div
        ranking_divs = await page.query_selector_all('div.css-1779w6t')

        print("지금 많이 찾는 검색어 Top 10:")
        for div in ranking_divs[:10]:
            # div 내 첫 번째 span: 순위
            span_tags = await div.query_selector_all("span")
            rank = await span_tags[0].inner_text() if span_tags else "?"

            # 검색어 텍스트
            keyword_span = await div.query_selector("a span")
            keyword = await keyword_span.inner_text() if keyword_span else "?"

            print(f"{rank}. {keyword}")

        await browser.close()

asyncio.run(main())