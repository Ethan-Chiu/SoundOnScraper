import asyncio
import json
from playwright.sync_api import sync_playwright, Playwright


def run(playwright: Playwright, url: str):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()

    with page.expect_response(lambda response: "episode" in response.url) as response_info:
        page.goto(url)
    response = response_info.value
    json_data = response.json()

    browser.close()

    # print(json_data)
    # print(json.dumps(json_data, ensure_ascii=False, indent=4))

    # status = json_data["status"]
    # print(status == 200)

    data = json_data["data"]
    return data

    # print(len(data))

    print(json.dumps(data[0], ensure_ascii=False, indent=4))
    # print(data[0]['data']['audioUrl'])
    

def get_channel_episodes(url: str):
    with sync_playwright() as playwright:
        data = run(playwright, url)
    return data

def main():
    url = "https://player.soundon.fm/p/511455c6-f5ee-4e8f-aac3-912b277c0efe"
    with sync_playwright() as playwright:
        run(playwright, url)

main()
