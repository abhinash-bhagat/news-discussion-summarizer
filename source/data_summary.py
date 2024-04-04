import nltk
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def summarize_discussion(comments):
    # Tokenize the comments into sentences
    sentences = sent_tokenize(comments)
    
    # Tokenize words and remove stopwords
    words = word_tokenize(comments.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # Calculate word frequencies
    word_freq = FreqDist(words)
    
    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        sentence_score = 0
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                sentence_score += word_freq[word]
        sentence_scores[sentence] = sentence_score
    
    # Get top 1% of sentences by score
    num_sentences = max(int(len(sentences) * 0.01), 1) # Ensure at least 1 sentence is selected
    top_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    # Join top sentences to create summary
    summary = ' '.join(top_sentences)
    
    return summary




def summarize_viewpoints(comments):
    # Extract positive, negative, and neutral comments
    positive_comments = comments.get('Positive', [])
    negative_comments = comments.get('Negative', [])
    neutral_comments = comments.get('Neutral', [])
    
    # Summarize each category of comments separately
    positive_summary = summarize_discussion(' '.join(positive_comments))
    negative_summary = summarize_discussion(' '.join(negative_comments))
    neutral_summary = summarize_discussion(' '.join(neutral_comments))
    
    return positive_summary, negative_summary, neutral_summary

def present_information(topic, positive_summary, negative_summary, neutral_summary):
    print(f"Topic: {topic}")
    print("Positive Viewpoints:")
    print(positive_summary)
    print("Negative Viewpoints:")
    print(negative_summary)
    print("Neutral Viewpoints:")
    print(neutral_summary)

# Load JSON data
json_file_path = 'data\extracted_data.json'
data = load_json_data(json_file_path)

if data:
    for topic, comments_info in data.items():
        # Summarize diverse viewpoints
        positive_summary, negative_summary, neutral_summary = summarize_viewpoints(comments_info)
        
        # Present the information
        present_information(topic, positive_summary, negative_summary, neutral_summary)
else:
    print("Failed to load JSON data.")