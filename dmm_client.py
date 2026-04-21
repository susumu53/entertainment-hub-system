import requests
import re
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

class DMMClient:
    def __init__(self):
        self.api_id = os.getenv("DMM_API_ID")
        self.affiliate_id = os.getenv("DMM_AFFILIATE_ID")
        self.base_url = "https://api.dmm.com/affiliate/v3/ItemList"

    def _clean_title(self, title):
        title = re.sub(r'[\(（].*?[\)）]', '', title)
        title = re.sub(r'[「」『』【】]', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        return title

    def get_youtube_video_id(self, query):
        """YouTubeを検索して公式PV等の動画IDを取得"""
        try:
            search_query = f"{query} 公式 PV 予告"
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            r = requests.get(url, headers=headers, timeout=10)
            
            match = re.search(r'\"videoRenderer\":\{\"videoId\":\"(.*?)\"', r.text)
            if match: return match.group(1)
            
            match = re.search(r'watch\?v=([a-zA-Z0-9_-]{11})', r.text)
            if match: return match.group(1)
        except Exception as e:
            print(f"YouTube search failed for {query}: {e}")
        return None

    def get_items(self, service=None, floor=None, hits=20, sort="rank", keyword=None):
        params = {
            "api_id": self.api_id,
            "affiliate_id": self.affiliate_id,
            "site": "DMM.com",
            "hits": hits,
            "sort": sort,
            "output": "json"
        }
        if service: params["service"] = service
        if floor: params["floor"] = floor
        if keyword: params["keyword"] = keyword

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            if "result" in data and "items" in data["result"]:
                return data["result"]["items"]
        except Exception as e:
            print(f"DMM API Error: {e}")
        return []

    def get_free_manga(self, hits=30):
        """0円の漫画・電子書籍を取得"""
        items = self.get_items(service="ebook", floor="comic", hits=hits, sort="rank")
        
        free_items = []
        for item in items:
            price = str(item.get("prices", {}).get("price", "9999"))
            if "0" in price and "10" not in price: # 0円判定
                free_items.append(item)
        
        return free_items
