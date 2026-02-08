import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://birmarket.az/categories/2627-temir-ve-tikinti"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ScraperBot/1.0)"
}

def scrape_all_pages():
    page = 1
    products = []

    while True:
        url = f"{BASE_URL}?page={page}"
        print(f"[+] Oxunur: səhifə {page}")

        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            break

        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("div.product-item")

        if not items:
            break

        for item in items:
            try:
                name = item.select_one("a.product-title").text.strip()

                price_tag = item.select_one("span.price")
                price = price_tag.text.strip() if price_tag else "Qiymət yoxdur"

                review_tag = item.select_one("span.review-count")
                reviews = int(review_tag.text.strip("()")) if review_tag else 0

                products.append({
                    "name": name,
                    "price": price,
                    "reviews": reviews
                })
            except Exception:
                continue

        page += 1
        time.sleep(1)  # etik crawling

    return products

def save_csv(products, filename="top_products.csv"):
    products.sort(key=lambda x: x["reviews"], reverse=True)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "reviews"])
        writer.writeheader()
        writer.writerows(products)

    print(f"\n✅ Fayl yaradıldı: {filename}")

def main():
    products = scrape_all_pages()
    save_csv(products)

    print("\n🔥 TOP 10 məhsul:\n")
    for i, p in enumerate(products[:10], 1):
        print(f"{i}. {p['name']} | {p['price']} | Rəy: {p['reviews']}")

if __name__ == "__main__":
    main()
