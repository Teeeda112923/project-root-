import os
import feedparser
import random
import tweepy

# === APIキーと環境変数読み込み ===
consumer_key = os.environ.get('X_API_KEY')
consumer_secret = os.environ.get('X_API_SECRET')
access_token = os.environ.get('X_ACCESS_TOKEN')
access_token_secret = os.environ.get('X_ACCESS_SECRET')
feed_url = os.environ.get('FEED_URL')
hashtags = os.environ.get('HASHTAGS', '')
status_prefix = os.environ.get('STATUS_PREFIX', '【アーカイブ】')
test_mode = os.environ.get('TEST_MODE', 'false').lower() == 'true'

# === デバッグ出力 ===
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
def post_to_x(title, link):
    print("🐦 投稿準備中...")

    status = f"{status_prefix}\n{title}\n{link}"
    if hashtags:
        status += f"\n\n{hashtags}"

    print("📤 投稿内容:")
    print(status)

    if test_mode:
        print("🧪 TEST_MODE: 投稿せずログ出力のみ")
        return

    try:
        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        response = client.create_tweet(text=status)
        print("✅ 投稿成功")
        print(response)
    except tweepy.errors.Forbidden as e:
        print(f"❌ 投稿エラー（403 Forbidden）: {e}")
        print("⚠️ API権限不足。Essentialプランなどでは制限があります。")
    except tweepy.errors.Unauthorized as e:
        print(f"❌ 認証エラー（401 Unauthorized）: {e}")
        print("⚠️ アクセストークンが無効または期限切れの可能性あり。")
    except Exception as e:
        print(f"❌ その他の投稿エラー: {e}")
        raise

# === メイン処理 ===
def main():
    title, link = get_random_article(feed_url)
    post_to_x(title, link)

if __name__ == "__main__":
    main()
