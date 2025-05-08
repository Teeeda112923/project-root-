import os
import feedparser
import random
import openai
import tweepy

# === APIキー読み込み ===
consumer_key = os.environ.get('X_API_KEY')
consumer_secret = os.environ.get('X_API_SECRET')
access_token = os.environ.get('X_ACCESS_TOKEN')
access_token_secret = os.environ.get('X_ACCESS_SECRET')
openai.api_key = os.environ.get('OPENAI_API_KEY')

# === カスタム環境変数 ===
feed_url = os.environ.get('FEED_URL', 'https://example.com/feed')
hashtags = os.environ.get('HASHTAGS', '#example').strip()
status_prefix = os.environ.get('STATUS_PREFIX', '【アーカイブ】').strip()
test_mode = os.environ.get('TEST_MODE', 'false').lower() == 'true'

print("🔐 APIキー確認:")
print(f"X_API_KEY: {'OK' if consumer_key else 'NG'}")
print(f"X_API_SECRET: {'OK' if consumer_secret else 'NG'}")
print(f"X_ACCESS_TOKEN: {'OK' if access_token else 'NG'}")
print(f"X_ACCESS_SECRET: {'OK' if access_token_secret else 'NG'}")
print(f"FEED_URL: {feed_url}")
print(f"HASHTAGS: {hashtags}")
print(f"STATUS_PREFIX: {status_prefix}")
print(f"TEST_MODE: {'ON' if test_mode else 'OFF'}")

# === RSS取得と記事抽出 ===
def get_random_article(feed_url):
    print(f"🌐 RSSフィードを取得: {feed_url}")
    feed = feedparser.parse(feed_url)
    entries = feed.entries
    if not entries:
        raise Exception("❌ RSSフィードから記事が取得できません")
    selected = random.choice(entries)
    print(f"🎯 選ばれた記事: {selected.title} / {selected.link}")
    return selected.title, selected.link

# === 投稿処理 ===
def post_to_x(title, link):
    print("🐦 投稿準備中...")
    status = f"{status_prefix}\n{title}\n{link}\n{hashtags}"
    print("📤 投稿内容:\n" + status)

    if test_mode:
        print("🧪 TEST_MODE: 投稿せずログ出力のみ")
        return

    try:
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(status=status)
        print("✅ 投稿成功")
    except Exception as e:
        print(f"❌ 投稿エラー: {e}")
        raise

# === メイン処理 ===
def main():
    title, link = get_random_article(feed_url)
    post_to_x(title, link)

if __name__ == "__main__":
    main()
