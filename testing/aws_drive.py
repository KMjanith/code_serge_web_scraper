from playwright.sync_api import sync_playwright

# List of target sections
target_sections = [
    "What is AWS Lambda?",
    "Example apps",
    "Building with TypeScript",
    "Integrating other services",
    "Code examples"
]

def scrape_target_sections_with_main():
    with sync_playwright() as p:
        # Launch headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the AWS Lambda documentation
        page.goto("https://docs.aws.amazon.com/lambda/latest/dg/welcome.html")

        # Wait for the sidebar menu to load
        page.wait_for_selector("nav")

        # Locate all sidebar items
        menu_items = page.locator("nav ul li a")  # Sidebar links
        all_texts = menu_items.all_text_contents()  # Extract visible texts
        all_links = menu_items.evaluate_all("elements => elements.map(e => e.href)")  # Extract URLs

        # Dictionary to hold target sections and their <main> content
        target_data = {}

        for section, link in zip(all_texts, all_links):
            if section in target_sections:
                # Navigate to the section URL
                page.goto(link)
                page.wait_for_selector("main")  # Wait for the <main> tag to render
                
                # Extract the content of the <main> tag
                main_content = page.locator("main").inner_html()  # Get raw HTML inside <main>
                
                # Store the section, URL, and <main> content
                target_data[section] = {
                    "url": link,
                    "main_content": main_content.strip()  # Clean up extra spaces
                }

        # Close the browser
        browser.close()

        # Print the scraped sections and <main> content
        for section, details in target_data.items():
            print(f"Section: {section}")
            print(f"URL: {details['url']}")
            print("Main Content:")
            print(details['main_content'])  # Print a preview of <main> content (first 500 chars)
            print("...")  # Indicate truncated content
            print()

if __name__ == "__main__":
    scrape_target_sections_with_main()
