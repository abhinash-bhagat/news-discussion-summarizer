# Getting latest news topics in a city
import requests
def get_top_news_topics(city):
    api_key = 'f76262fe43db48ec88b360bad4e560bd'
    url = f'https://newsapi.org/v2/top-headlines?q={city}&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            topics = []
            articles = data.get('articles', [])
            
            for article in articles[:15]:  # Extract top 5 articles
                topics.append(article['title'])
            
            return topics
        else:
            print(f"Error: {data['message']}")
            return None
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


# Fetching Reddit Discussions
import praw
def fetch_comments_from_reddit(post_id):
    reddit = praw.Reddit(user_agent=True, client_id="dmoPjIG2Htcj5fXH8o9ufA", 
                         client_secret="cA_5xyFiuEOJ4AuGmbLd82GnOTk-qA", username='abhinash-', password='Abhinash143')

    submission = reddit.submission(id=post_id)
    comments = []
    # Limit the number of comments to retrieve
    comment_limit = 15
    submission.comments.replace_more(limit=3)
    for comment in submission.comments[:comment_limit]:
        comments.append(comment.body)
    
    return comments


# Saving categorized comments as json
from textblob import TextBlob
# Function to identify viewpoints (positive, negative, neutral)
def identify_viewpoints(comments):
    positive_comments = []
    negative_comments = []
    neutral_comments = []
    
    for comment in comments:
        analysis = TextBlob(comment)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0:
            positive_comments.append(comment)
        elif polarity < 0:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)
    
    return positive_comments, negative_comments, neutral_comments

city = "New York"
news_topics = get_top_news_topics(city)
if news_topics:
    reddit = praw.Reddit(user_agent=True, client_id="dmoPjIG2Htcj5fXH8o9ufA", 
                         client_secret="cA_5xyFiuEOJ4AuGmbLd82GnOTk-qA", username='abhinash-', password='Abhinash143')
    
    # Initialize an empty dictionary to store data
    extracted_data = {}
    
    for topic in news_topics:
        print(f"POST: {topic}")
        # Search Reddit for posts related to the news topic in r/news and r/politics subreddits
        subreddit_names = ["news", "politics"]
        for subreddit_name in subreddit_names:
            subreddit = reddit.subreddit(subreddit_name)
            search_results = subreddit.search(topic, sort="new", limit=15, time_filter="week")  # Search top 15 latest posts
            for submission in search_results:
                comments = fetch_comments_from_reddit(submission.id)
                if comments:
                    # Classify comments into positive, negative, neutral
                    positive_comments, negative_comments, neutral_comments = identify_viewpoints(comments[-14:])
                    
                    # Store the post title and classified comments in the dictionary
                    extracted_data[submission.title] = {
                        "Positive": positive_comments,
                        "Negative": negative_comments,
                        "Neutral": neutral_comments
                    }
                else:
                    print(f"No comments retrieved for post: {submission.title} (Subreddit: {subreddit_name})")
    
    # Print the extracted data
    print("Extracted data:")
    print(extracted_data)
    import json
    # Save the extracted data to a JSON file
    with open("data\extracted_data.json", "w") as json_file:
        json.dump(extracted_data, json_file, indent=4)
        
    print("Data saved successfully to: extracted_data.json")
else:
    print("Failed to fetch news topics.")