from googleapiclient.discovery import build

# ===================================
# YOUTUBE API KEY
# ===================================

YOUTUBE_API_KEY = "YOUR_API_KEY_HERE"

# ===================================
# CREATE YOUTUBE CLIENT
# ===================================

youtube = build(

    "youtube",

    "v3",

    developerKey=YOUTUBE_API_KEY
)

# ===================================
# SEARCH VIDEO
# ===================================

def search_youtube_video(topic):

    try:

        request = youtube.search().list(

            q=f"{topic} tutorial",

            part="snippet",

            maxResults=1,

            type="video"
        )

        response = request.execute()

        items = response.get(
            "items",
            []
        )

        if not items:

            return None

        video = items[0]

        video_id = video["id"]["videoId"]

        title = video["snippet"]["title"]

        url = (

            f"https://www.youtube.com/watch?v={video_id}"
        )

        return {

            "title": title,

            "url": url
        }

    except Exception as e:

        print(e)

        return None