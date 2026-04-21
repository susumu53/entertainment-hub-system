class ArticleBuilder:
    def __init__(self):
        self.primary_color = "#311b92"
        self.accent_color = "#ff4081"

    def generate_html(self, item, ai_review, video_id=None):
        title = item.get('title', '')
        img_url = item.get('imageURL', {}).get('large', '')
        aff_url = item.get('affiliateURL', '')
        price = str(item.get('prices', {}).get('price', '---'))
        list_price = str(item.get('prices', {}).get('list_price', price))
        avg_score = item.get('review', {}).get('average', '0.0')
        
        # Tags/Genres
        genres = ", ".join([g.get('name') for g in item.get('iteminfo', {}).get('genre', [])[:5]])

        # Progress bar color
        score_val = float(avg_score) * 20 # 5.0 -> 100%
        
        video_html = ""
        if video_id:
            video_html = f"""
            <div style="margin: 30px 0; background: #000; border-radius: 12px; overflow: hidden; position: relative; padding-top: 56.25%;">
                <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" 
                    src="https://www.youtube.com/embed/{video_id}" allowfullscreen></iframe>
            </div>
            """

        return f"""
<div style="padding: 20px; background: #fdfdfd; font-family: 'Helvetica Neue', Arial, sans-serif; color: #333; max-width: 700px; margin: 0 auto;">
    <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, {self.primary_color} 0%, #673ab7 100%); color: #fff; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
        <div style="font-size: 0.85em; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; opacity: 0.8;">Entertainment AI Selection</div>
        <h1 style="margin: 0; font-size: 1.7em; line-height: 1.4;">{title}</h1>
    </div>

    <div style="text-align: center; margin-bottom: 30px;">
        <img src="{img_url}" style="max-width: 100%; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.08);">
    </div>

    <div style="background: #fff; border-radius: 15px; padding: 25px; border: 1px solid #eee; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); position: relative;">
        <div style="position: absolute; top: -12px; left: 20px; background: {self.accent_color}; color: #fff; padding: 3px 12px; border-radius: 20px; font-size: 0.75em; font-weight: bold;">AI EDITOR'S VOICE</div>
        <div style="font-size: 1.05em; line-height: 1.7; color: #444; font-style: italic;">
            「{ai_review}」
        </div>
        <div style="margin-top: 20px; border-top: 1px dashed #eee; padding-top: 15px;">
            <div style="font-size: 0.85em; color: #888; margin-bottom: 5px;">User Satisfaction Index</div>
            <div style="background: #efefef; height: 8px; border-radius: 4px; overflow: hidden;">
                <div style="background: {self.accent_color}; width: {score_val}%; height: 100%;"></div>
            </div>
            <div style="text-align: right; color: #ffb400; font-weight: bold; margin-top: 5px;">★ {avg_score} / 5.0</div>
        </div>
    </div>

    {video_html}

    <div style="margin-bottom: 30px; font-size: 0.9em; color: #666;">
        <strong>ジャンル:</strong> {genres}
    </div>

    <div style="background: #fce4ec; border-radius: 15px; padding: 25px; text-align: center; border: 1px solid #f8bbd0;">
        <div style="font-size: 1.4em; font-weight: bold; color: #c2185b; margin-bottom: 20px;">
            価格： {price} 円
            <span style="font-size: 0.6em; color: #999; text-decoration: line-through; margin-left: 8px;">(定価: {list_price}円)</span>
        </div>
        <a href="{aff_url}" target="_blank" style="display: inline-block; background: {self.accent_color}; color: #fff; padding: 16px 45px; border-radius: 30px; text-decoration: none; font-weight: bold; font-size: 1.25em; box-shadow: 0 8px 20px rgba(255,64,129,0.25);">公式サイトで作品を見る ＞</a>
    </div>

    <div style="text-align: center; margin-top: 40px; color: #aaa; font-size: 0.75em; line-height: 1.6;">
        ※掲載情報は自動解析によるものです。最新情報は公式サイトにてご確認ください。<br>
        © Entertainment Hub AI System / DMM Affiliate
    </div>
</div>
"""
