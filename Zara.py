import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            locale="ko-KR",
            timezone_id="Asia/Seoul",
            viewport={"width": 1200, "height": 800}
        )

        page = await context.new_page()
        await page.goto("https://www.zara.com/kr/ko/woman-new-in-l1180.html?v1=2546081", wait_until="load")
        await page.wait_for_timeout(3000)

        # 스크롤 유도 (lazy loading)
        for _ in range(15):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

        image_tags = await page.query_selector_all('img[data-qa-qualifier="media-image"]')
        print(f" 최종 이미지 수: {len(image_tags)}개")

        for i, img in enumerate(image_tags):
            src = await img.get_attribute("src")
            alt = await img.get_attribute("alt")
            print(f"\n🖼️ 이미지 {i+1}")
            print(f"   🔗 URL: {src}")
            print(f"   🏷️ ALT: {alt}")

        await browser.close()

asyncio.run(main())