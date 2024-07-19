import asyncio
import json
from playwright.async_api import async_playwright, Playwright

url = "https://player.soundon.fm/p/511455c6-f5ee-4e8f-aac3-912b277c0efe"

responses = []

def on_response(response):
    responses.append(response)

async def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch()
    page = await browser.new_page()
    # Subscribe to "request" and "response" events.
    # page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", on_response)
    async with page.expect_response(lambda response: "episode" in response.url) as response_info:
        await page.goto(url)
    response = await response_info.value
    json_data = await response.json()

    print(json_data["status"])

    data = json_data["data"]

    print(len(data))

    print(json.dumps(data[0], ensure_ascii=False, indent=4))
    print(data[0]['data']['audioUrl'])
    

    # await page.goto(url)
    # await page.wait_for_load_state("networkidle") 
    # for res in responses:
    #     print(res.status, res.url)
    #     if "episode" in res.url and res.status == 200:
    #         try:
    #             json = await res.text()
    #             print(json[:500])
    #         except e:
    #             print(e)

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
