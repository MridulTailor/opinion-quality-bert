import urllib.request
import urllib.parse
import json
import csv
import time
import random

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('RAPIDAPI_KEY', 'your_api_key_here')
HOST = 'reddit34.p.rapidapi.com'

def fetch_top_posts():
    url = 'https://reddit34.p.rapidapi.com/getTopPostsBySubreddit?subreddit=nba&time=month'
    req = urllib.request.Request(url, headers={'x-rapidapi-key': API_KEY, 'x-rapidapi-host': HOST})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            posts = res.get('data', {}).get('posts', [])
            return ['https://www.reddit.com' + p['data']['permalink'] for p in posts if 'permalink' in p['data']]
    except Exception as e:
        print("Error fetching top posts:", e)
        return []

def fetch_comments(post_url):
    encoded_url = urllib.parse.quote(post_url, safe='')
    url = f'https://reddit34.p.rapidapi.com/getPostCommentsWithSortV2?post_url={encoded_url}&sort=top'
    req = urllib.request.Request(url, headers={'x-rapidapi-key': API_KEY, 'x-rapidapi-host': HOST})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            comments = res.get('data', {}).get('comments', [])
            texts = []
            for c in comments:
                if 'body' in c:
                    texts.append(c['body'].replace('\n', ' ').strip())
            return texts
    except Exception as e:
        print(f"Error fetching comments for {post_url}:", e)
        return []

def main():
    print("Fetching top r/nba posts...")
    post_urls = fetch_top_posts()
    print(f"Found {len(post_urls)} posts. Fetching comments...")
    
    all_comments = []
    for url in post_urls[:5]:
        comments = fetch_comments(url)
        all_comments.extend(comments)
        time.sleep(1)
        
    all_comments = list(set([c for c in all_comments if 20 < len(c) < 1500]))
    print(f"Collected {len(all_comments)} unique, valid-length comments.")
    
    analysis = []
    hot_takes = []
    reactions = []
    
    for c in all_comments:
        if len(c) > 300 or " stats " in c.lower() or " rating " in c.lower():
            analysis.append(c)
        elif len(c) < 100:
            reactions.append(c)
        else:
            hot_takes.append(c)
            
    min_class_size = min(len(analysis), len(hot_takes), len(reactions), 80)
    print(f"Balancing classes to {min_class_size} each...")
    
    dataset = []
    dataset.extend([{'text': t, 'label': 'analysis', 'notes': ''} for t in random.sample(analysis, min_class_size)])
    dataset.extend([{'text': t, 'label': 'hot_take', 'notes': ''} for t in random.sample(hot_takes, min_class_size)])
    dataset.extend([{'text': t, 'label': 'reaction', 'notes': ''} for t in random.sample(reactions, min_class_size)])
    
    random.shuffle(dataset)
    
    with open('dataset.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['text', 'label', 'notes'])
        for row in dataset:
            writer.writerow([row['text'], row['label'], row['notes']])
            
    print(f"Saved {len(dataset)} perfectly balanced REAL reddit examples to dataset.csv.")

if __name__ == '__main__':
    main()
