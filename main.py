import json
import csv
import os
import requests
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Fetch API credentials from environment
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = os.getenv("NEWS_API_URL")

# Store latest articles globally
articles = []

# Save fetched data to tech_news.json
def save_to_json(data, filename="tech_news.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[✔] Articles saved to {filename}")

# Export current articles to CSV
def export_to_csv(filename="tech_news.csv"):
    if not articles:
        print("[!] No articles to export. Fetch news first.")
        return
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Source", "Published At", "URL"])
        for article in articles:
            writer.writerow([
                article["title"],
                article["source"]["name"],
                article["publishedAt"],
                article["url"]
            ])
    print(f"[✔] Articles exported to {filename}")

# Display all articles
def show_articles(data):
    if not data:
        print("[!] No articles to show.")
        return
    for i, article in enumerate(data, start=1):
        print(f"\n📄 Article {i}")
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']['name']}")
        print(f"Published At: {article['publishedAt']}")
        print(f"URL: {article['url']}")

# Fetch latest tech news
def fetch_news():
    global articles
    if not NEWS_API_KEY or not NEWS_API_URL:
        print("[✖] Missing API key or URL in environment.")
        return
    try:
        response = requests.get(NEWS_API_URL, params={
            "category": "technology",
            "language": "en",
            "apiKey": NEWS_API_KEY
        })
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        if articles:
            print(f"[✔] Fetched {len(articles)} articles.")
            save_to_json(articles)
        else:
            print("[!] No articles found.")
    except requests.RequestException as e:
        print(f"[✖] Error fetching news: {e}")

# Filter articles by keyword
def filter_articles():
    if not articles:
        print("[!] No articles to filter. Fetch news first.")
        return
    keyword = input("Enter keyword to filter by: ").lower()
    filtered = [a for a in articles if keyword in a['title'].lower()]
    if filtered:
        print(f"[✔] Found {len(filtered)} article(s) with '{keyword}':")
        show_articles(filtered)
    else:
        print(f"[!] No articles found with '{keyword}'.")

# CLI Menu
def show_menu():
    print("\n=== 📰 Tech News Aggregator ===")
    print("1. Fetch latest tech news")
    print("2. Show all articles")
    print("3. Filter articles by keyword")
    print("4. Export articles to CSV")
    print("5. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            fetch_news()
        elif choice == "2":
            show_articles(articles)
        elif choice == "3":
            filter_articles()
        elif choice == "4":
            export_to_csv()
        elif choice == "5":
            print("Goodbye, Eric!")
            break
        else:
            print("[!] Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
