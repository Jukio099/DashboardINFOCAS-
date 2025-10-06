import asyncio
from playwright.async_api import async_playwright, expect

async def run_verification_with_logs():
    """
    Launches a browser, captures console logs, and takes a screenshot.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Listen for all console events and print them
        page.on("console", lambda msg: print(f"CONSOLE LOG: {msg.text}"))

        try:
            # Navigate to the URL of the dashboard
            await page.goto("http://127.0.0.1:8057/", timeout=30000)

            # Wait for the main heading to be visible
            await expect(page.get_by_role("heading", name="Dashboard de Competitividad de Casanare")).to_be_visible(timeout=15000)

            # Wait for at least one iframe to be present, even if not visible
            await page.wait_for_selector("iframe[id='grafico-sectores']", timeout=15000)

            # Give it a moment to try and render
            await page.wait_for_timeout(3000)

            # Take a full-page screenshot to capture everything
            screenshot_path = "jules-scratch/verification/dashboard_final_view.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"An error occurred during verification: {e}")

        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_verification_with_logs())