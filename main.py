import os
import datetime
import json
import time
from dmm_client import DMMClient
from seesaa_poster import SeesaaPoster
from ai_reviewer import AIReviewer
from article_builder import ArticleBuilder

class EntertainmentAutoPost:
    def __init__(self):
        self.dmm = DMMClient()
        self.seesaa = SeesaaPoster()
        self.ai = AIReviewer()
        self.builder = ArticleBuilder()
        self.log_file = "posted_log.json"
        self._load_log()

    def _load_log(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                self.posted_ids = json.load(f)
        else:
            self.posted_ids = []

    def _save_log(self, item_id):
        self.posted_ids.append(item_id)
        # Keep last 1000 items
        if len(self.posted_ids) > 1000:
            self.posted_ids = self.posted_ids[-1000:]
        with open(self.log_file, "w") as f:
            json.dump(self.posted_ids, f)

    def run_task(self):
        hour = datetime.datetime.now().hour
        print(f"Executing task for hour: {hour}")

        if hour % 2 == 1:
            # 奇数時: 無料マンガ・電子書籍
            print("Category: Free Manga / eBooks")
            items = self.dmm.get_free_manga(hits=20)
            category = ["無料マンガ", "電子書籍セール"]
        else:
            # 偶数時: 注目TV作品・アニメ・ゲーム
            print("Category: Trending TV / Anime / Games")
            if hour % 4 == 0:
                items = self.dmm.get_items(service="dmmtv", floor="dmmtv_video", hits=20)
                category = ["アニメ・動画", "DMM TV"]
            else:
                items = self.dmm.get_items(service="pcsoft", floor="digital_pcgame", hits=20)
                category = ["ゲーム", "PCゲーム"]

        # 未投稿のアイテムを探す
        target_item = None
        for item in items:
            cid = item.get("content_id")
            if cid not in self.posted_ids:
                target_item = item
                break
        
        if not target_item:
            print("No new items found. Skipping...")
            return

        print(f"Topic: {target_item['title']}")
        
        # YouTube動画取得
        video_id = self.dmm.get_youtube_video_id(self.dmm._clean_title(target_item['title']))
        
        # AIレビュー生成
        avg_score = target_item.get('review', {}).get('average', '0.0')
        ai_review = self.ai.generate_review(target_item['title'], "", avg_score)
        
        # HTML生成
        html = self.builder.generate_html(target_item, ai_review, video_id)
        
        # 投稿
        title = f"【期間限定】AI厳選エンタメ情報：{target_item['title']}"
        post_id = self.seesaa.post_article(title, html, categories=category)
        
        if post_id:
            self._save_log(target_item.get("content_id"))
            print(f"Success! Post ID: {post_id}")

if __name__ == "__main__":
    app = EntertainmentAutoPost()
    app.run_task()
