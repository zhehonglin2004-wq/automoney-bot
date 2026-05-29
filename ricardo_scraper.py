import requests
from bs4 import BeautifulSoup
import time

def scrape_ricardo(search_query):
    base_url = "https://www.ricardo.ch/de/s/"
    url = f"{base_url}{search_query.replace(' ', '-')}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        items = soup.find_all("div", class_="item")
        results = []
        for item in items[:10]:
            try:
                title = item.find("h3", class_="item-title").text.strip()
                price = item.find("div", class_="price").text.strip()
                link = "https://www.ricardo.ch" + item.find("a")["href"]
                results.append({"title": title, "price": price, "link": link})
            except:
                continue
        return results
    except Exception as e:
        print(f"Fehler: {e}")
        return []

if __name__ == "__main__":
    # 你可以改成客户想要的关键词，比如 "iphone 15", "macbook pro"
    search_term = "macbook pro"
    print(f"Suche nach: {search_term} auf Ricardo...")
    data = scrape_ricardo(search_term)
    
    if data:
        print("\nGefundene Angebote:")
        for idx, offer in enumerate(data, 1):
            print(f"{idx}. {offer['title']}")
            print(f"   Preis: {offer['price']}")
            print(f"   Link: {offer['link']}\n")
    else:
        print("Keine Angebote gefunden oder Fehler beim Scrapen.")
