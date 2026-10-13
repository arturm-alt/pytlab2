import csv
import json
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://quotes.toscrape.com/js/")
        
        data = []
        
        while True:
            page.wait_for_selector(".quote")
            
            for quote in page.query_selector_all(".quote"):
                text = quote.query_selector(".text").inner_text().strip()
                author = quote.query_selector(".author").inner_text().strip()
                tags = [t.inner_text().strip() for t in quote.query_selector_all(".tag")]
                
                data.append({"author": author, "quote": text, "tags": tags})
            
            next_button = page.query_selector(".next > a")
            if next_button:
                next_button.click()
            else:
                break
            
        browser.close()
        
    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["author", "quote", "tags"])
        writer.writeheader()
        for row in data:
            row_copy = row.copy()
            row_copy["tags"] = ", ".join(row_copy["tags"])
            writer.writerow(row_copy)

if __name__ == "__main__":
    main()
