import json
import time
from datetime import datetime
from google_play_scraper import app as gp_app_detail
from google_play_scraper.constants.google_play import Sort
import google_play_scraper

REGIONS = {
    "TW": {"lang": "zh-TW"},
    "HK": {"lang": "zh-HK"},
    "MO": {"lang": "zh-TW"},
    "JP": {"lang": "ja"},
    "KR": {"lang": "ko"}
}

CHARTS = {
    "free":     "topselling_free",
    "grossing": "topgrossing"
}

def fetch_gp_chart(country, lang, chart_key):
    try:
        from google_play_scraper import top_charts
        results = top_charts(
            chart=CHARTS[chart_key],
            category=google_play_scraper.constants.google_play.Category.GAME,
            country=country,
            lang=lang,
            n=15
        )
        return [{"name": r.get("title",""), "dev": r.get("developer","")}
                for r in results if r.get("title")]
    except ImportError:
        pass

    try:
        from google_play_scraper import collection
        results = collection(
            collection_name=CHARTS[chart_key],
            category_name="GAME",
            country=country,
            lang=lang,
            count=15
        )
        return [{"name": r.get("title",""), "dev": r.get("developer","")}
                for r in results if r.get("title")]
    except Exception as e:
        print(f"[GP][{country}][{chart_key}] 失敗: {e}")
        return []

def main():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    output = {"date": today, "regions": {}}

    for cc, cfg in REGIONS.items():
        print(f"抓取 {cc}...")
        output["regions"][cc] = {
            "gp_free":     fetch_gp_chart(cc, cfg["lang"], "free"),
            "gp_grossing": fetch_gp_chart(cc, cfg["lang"], "grossing")
        }
        time.sleep(1)

    with open("charts.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("完成！charts.json 已輸出")

if __name__ == "__main__":
    main()
