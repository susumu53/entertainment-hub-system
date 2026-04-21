import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AIReviewer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def generate_review(self, title, description="", rating="0.0"):
        if not self.model:
            return "非常に完成度が高い作品です。特にキャラクターの描写が深く、一気に読み進めてしまう魅力があります。"

        prompt = f"""
以下の作品情報を元に、アフィリエイトブログに掲載する「プロの書評家による推薦レビュー」を200文字程度で作成してください。
読者がワクワクし、すぐにチェックしたくなるようなポジティブな文章にしてください。

【作品タイトル】: {title}
【内容紹介】: {description[:500]}
【ユーザー評価】: {rating} / 5.0

制約:
- 「{title}」を必ず含めてください。
- プロフェッショナルかつ情熱的なトーンで。
- 日本語で作成。
"""
        try:
            response = self.model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini Error: {e}")
            
        return f"「{title}」は、圧倒的な筆致で描かれたエンターテインメントの傑作です。今すぐ手に取るべき一冊です。"
