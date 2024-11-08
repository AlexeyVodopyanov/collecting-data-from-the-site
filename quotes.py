import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes(base_url="http://quotes.toscrape.com"):
    quotes = []
    page_url = base_url
    
    while page_url:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all quote containers
        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").get_text()
            author = quote.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
            
            quotes.append({
                "quote": text,
                "author": author,
                "tags": tags
            })
        
        next_btn = soup.find("li", class_="next")
        page_url = base_url + next_btn.find("a")["href"] if next_btn else None

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

    print("Quotes have been successfully scraped and saved to quotes.json")

scrape_quotes()
