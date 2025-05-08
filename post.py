import os
import feedparser
import random
import tweepy

# === APIキーと設定読み込み ===
consumer_key = os.environ.get('X_API_KEY')
consumer_secret = os.environ.get('X_API_SECRET')
access_token = os.environ.get('X_ACCESS_TOKEN')
access_token_secret = os.environ.get('X_ACCESS_SECRET')

feed_url = os.environ.get('FEED_URL')
hashtags_raw = os.environ.get('HASHTAGS', '')
status_prefix = os.environ.get('STATUS_PREFIX', '【アーカイブ】')
test_mode = os.environ.get('TEST_MODE') == 'true'

hashtags = ' '.join([f"#{tag.strip()}" for tag in hashtags_raw.split(',') if tag.strip()])

print("🔐 APIキー確認:")
print(f"X_API_KEY: {'OK' if consumer_key else 'NG'}")
print(f"X_API_SECRET: {'OK' if consumer_secret else 'NG'}")
print(f"X_ACCESS_TOKEN: {'OK' if access_token else 'NG'}")
print(f"X_ACCESS_SECRET: {'OK' if access_token_secret else 'NG'}")
print(f"FEED_URL: {feed_url if feed_url else 'NG'}")
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

# === X（旧Twitter）へ投稿 ===
def post_to_x(title, link):
    print("🐦 投稿準備中...")
    status = f"{status_prefix}\n{title}\n{link}\n\n{hashtags}"
    print("📤 投稿内容:")
    print(status)

    if test_mode:
        print("🧪 TEST_MODE: 投稿せずログ出力のみ")
        return

    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key, consumer_secret,
            access_token, access_token_secret
        )
        api = tweepy.API(auth)
        api.update_status(status=status)
        print("✅ 投稿成功")
    except tweepy.errors.Forbidden as e:
        print(f"❌ 投稿エラー: {e}")
        print("⚠️ 投稿権限がない可能性があります（v1.1 のみ使用可能）")
    except tweepy.errors.TooManyRequests as e:
        print(f"❌ レート制限エラー: {e}")
        print("⏳ 時間を置いて再試行してください")
    except Exception as e:
        print(f"❌ その他の投稿エラー: {e}")
        raise

# === メイン処理 ===
def main():
    if not feed_url:
        raise Exception("❌ FEED_URL が設定されていません")

    title, link = get_random_article(feed_url)
    post_to_x(title, link)

if __name__ == "__main__":
    main()
