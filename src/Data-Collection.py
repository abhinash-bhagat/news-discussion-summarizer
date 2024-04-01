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
            
            for article in articles[:5]:  # Extract top 5 articles
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
    comment_limit = 5
    submission.comments.replace_more(limit=3)
    for comment in submission.comments[:comment_limit]:
        comments.append(comment.body)
    
    return comments

city = "New York"
news_topics = get_top_news_topics(city)
if news_topics:
    reddit = praw.Reddit(user_agent=True, client_id="dmoPjIG2Htcj5fXH8o9ufA", 
                         client_secret="cA_5xyFiuEOJ4AuGmbLd82GnOTk-qA", username='abhinash-', password='Abhinash143')
    for topic in news_topics:
        print(f"\nComments for news topic: {topic}")
        # Search Reddit for posts related to the news topic in r/news and r/politics subreddits
        subreddit_names = ["news", "politics"]
        for subreddit_name in subreddit_names:
            subreddit = reddit.subreddit(subreddit_name)
            search_results = subreddit.search(topic, sort="new", limit=5)  # Search top 5 latest posts
            for submission in search_results:
                comments = fetch_comments_from_reddit(submission.id)
                if comments:
                    print(f"\nPost: {submission.title} (Subreddit: {subreddit_name})")
                    for comment in comments:
                        print(comment)
                else:
                    print(f"No comments retrieved for post: {submission.title} (Subreddit: {subreddit_name})")
else:
    print("Failed to fetch news topics.")