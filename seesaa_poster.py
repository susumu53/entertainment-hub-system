import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

class SeesaaPoster:
    def __init__(self):
        self.endpoint = "https://blog.seesaa.jp/rpc"
        self.email = os.getenv("SEESAA_EMAIL")
        self.password = os.getenv("SEESAA_PASSWORD")
        self.target_url = os.getenv("TARGET_BLOG_URL")
        self.client = xmlrpc.client.ServerProxy(self.endpoint)
        self._blog_id = None

    def get_blog_id(self):
        """指定されたURLに対応するBlog IDを取得する"""
        if self._blog_id:
            return self._blog_id
        
        try:
            blogs = self.client.blogger.getUsersBlogs("", self.email, self.password)
            if blogs:
                if self.target_url:
                    for blog in blogs:
                        if self.target_url.strip("/") in blog.get("url", ""):
                            self._blog_id = blog["blogid"]
                            break
                
                if not self._blog_id:
                    self._blog_id = blogs[0]['blogid']
                
                return self._blog_id
        except Exception as e:
            print(f"Failed to get Blog ID: {e}")
        return None

    def post_article(self, title, content, categories=None, tags=None):
        """記事を投稿する"""
        blog_id = self.get_blog_id()
        if not blog_id:
            return None

        post_data = {
            "title": title,
            "description": content,
        }
        
        if categories:
            post_data["categories"] = categories
        if tags:
            post_data["mt_keywords"] = ",".join(tags) if isinstance(tags, list) else tags

        try:
            # publish=True
            post_id = self.client.metaWeblog.newPost(blog_id, self.email, self.password, post_data, True)
            print(f"Successfully posted article: {post_id}")
            return post_id
        except Exception as e:
            print(f"Failed to post article: {e}")
            return None
