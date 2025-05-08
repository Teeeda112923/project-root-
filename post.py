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
feed_url = os.environ.get('FEED_URL')
hashtags = os.environ.get('HASHTAGS', '')
status_prefix = os.environ.get('STATUS_PREFIX', '【アーカイブ】')
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


# === X（Twitter）へ投稿（API v2）===
def post_to_x(title, link, comment):
    print("🐦 X(Twitter)へ投稿準備中...")
    try:
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        hashtags = "#cybernote #ブログ仲間と繋がりたい #Webライター"
        status = f"{status_prefix}\n{comment}\n\n{title}\n{link}\n\n{hashtags}"

        print("📤 投稿内容:")
        print(status)

        if os.environ.get('TEST_MODE') == 'true':
            print("🧪 TEST_MODE: 投稿せずログ出力のみ")
        else:
            response = client.create_tweet(text=status)
            print("✅ 投稿成功")
            print(response)
    except Exception as e:
        print(f"❌ 投稿エラー: {e}")
        raise

# === メイン処理 ===
def main():
    feed_url = "https://www.cybernote.click/?cat=4&feed=rss2"
    title, link = get_random_article(feed_url)
    comment = generate_comment(title)
    post_to_x(title, link, comment)

if __name__ == "__main__":
    main()
