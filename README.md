# Approach



## General Strategy:
The general strategy involved in this project was to gather and analyze discussions from Reddit related to various news topics. The process included fetching top news topics based on a specified city using NEWS API, searching for related posts on Reddit, extracting comments from these posts, categorizing the comments into positive, negative, and neutral viewpoints, and summarizing the discussions.

## Key Tools Considered:
    - Python: The primary programming language used for coding and scripting.
    - PRAW (Python Reddit API Wrapper): Used for interacting with Reddit's API to fetch posts and comments.
    - NLTK (Natural Language Toolkit): Utilized for text processing, including tokenization and sentiment analysis.
    - Streamlit: Employed for building a simple front-end to display the analyzed information on a webpage.

## Metrics for Evaluation:
The success of the project was evaluated based on the following metrics:

    - Accuracy of fetching top news topics from the specified city.
    - Effectiveness of gathering relevant discussions from Reddit.
    - Accuracy of sentiment analysis for categorizing comments into positive, negative, and neutral viewpoints.
    - Clarity and completeness of the summarized discussions presented to the user.


## README Instructions:
    - Clone the repository to your local machine.
    - Install the required dependencies listed in the requirements.txt file.
    - Run the Streamlit app using the command streamlit run app.py.
    - Enter the desired city name and click on the "Analyze Discussions" button.
    - View the summarized discussions displayed on the webpage.
