from googleapiclient.discovery import build
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# YouTube API key
api_key = "YOUR_API_KEY"

# YouTube video ID
video_id = "M9rqo776gV8"

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=100
)

response = request.execute()

comments = []

for item in response['items']:
    comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
    comments.append(comment)

df = pd.DataFrame(comments, columns=["Comment"])

def get_sentiment(comment):
    analysis = TextBlob(comment)

    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"

df["Sentiment"] = df["Comment"].apply(get_sentiment)
df.to_csv("youtube_comments_sentiment.csv", index=False)
print(df)

sentiment_count = df["Sentiment"].value_counts()

sentiment_count.plot(kind="bar")

plt.title("YouTube Comment Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Number of Comments")


plt.show()
