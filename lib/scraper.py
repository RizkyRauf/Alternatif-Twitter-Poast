# scraper.py
import time
import unicodedata
from datetime import datetime
from bs4 import BeautifulSoup
from lib.utils import ReadFile, save_to_json
from lib.twitter_poast import TwitterPost

class Scraper:
    """
    Kelas bertanggung jawab untuk mengikis pos Twitter.

    Metode:
        __init__: Menginisialisasi Scraper dengan URL dan jalur berkas kata kunci.
        scrape_tweets: Mengikis tweet berdasarkan kata kunci.
    """
    def __init__(self, url, path_file):
        """
        Menginisialisasi Scraper dengan URL dan jalur berkas kata kunci.

        Args:
            url (str): URL dari pengikis Twitter.
            path_file (str): Jalur ke berkas kata kunci.
        """
        self.url = url
        self.keyword_file = ReadFile.read_keywords_from_file(path_file)

    def scrape_tweets(self, key):
        """
        Mengikis tweet berdasarkan kata kunci.

        Args:
            key (str): Kata kunci untuk dicari dalam tweet.
        """
        driver = TwitterPost(self.url).initialize_driver()
        driver.get(self.url)
        if driver:
            formatted_tweets = []
            while True:
                driver.get(f"https://nitter.poast.org/search?f=tweets&q={key}")
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                tweets = soup.find_all('div', class_='timeline-item')
                
                if not tweets:
                    print("No tweets found. Scraping finished.")
                    break
                
                for tweet in tweets:
                    fullname = unicodedata.normalize('NFKD', tweet.find('a', class_='fullname').text).encode('ascii', 'ignore').decode('utf-8')
                    username = unicodedata.normalize('NFKD', tweet.find('a', class_='username').text).encode('ascii', 'ignore').decode('utf-8')
                    text = unicodedata.normalize('NFKD', tweet.find('div', class_='tweet-content media-body').text.strip()).encode('ascii', 'ignore').decode('utf-8')
                    link = tweet.find('a', class_='tweet-link')['href'].replace('#m', '') if tweet.find('a', class_='tweet-link') else ''
                    link = f"https://twitter.com{link}" if link else ''
                    date_element = tweet.find('span', class_='tweet-date').find('a') 
                    date_text = date_element['title'] if date_element else ''
                    formatted_date = datetime.strptime(date_text, '%b %d, %Y \u00b7 %I:%M %p UTC').strftime('%d/%m/%Y %H:%M:%S') if date_text else ''
                    tweet_stat = tweet.find('div', class_='tweet-stats')
                    stats = {}
                    if tweet_stat:
                        # Check if the 'icon-comment' element exists
                        comment_element = tweet_stat.select_one('.tweet-stat:nth-of-type(1) div.icon-container')
                        comment_count = comment_element.text.strip().replace(',', '') if comment_element.text.strip() else '0'
                                                
                        # Check if the 'retweet' element exists
                        retweet_element = tweet_stat.select_one('.tweet-stat:nth-of-type(2) div.icon-container')
                        retweet_count = retweet_element.text.strip().replace(',', '') if retweet_element.text.strip() else '0'
                                                
                        # Check if the 'icon-quote' element exists
                        quote_element = tweet_stat.select_one('.tweet-stat:nth-of-type(3) div.icon-container')
                        quote_count = quote_element.text.strip().replace(',', '') if quote_element.text.strip() else '0'
                                                
                        # Check if the 'icon-heart' element exists
                        heart_element = tweet_stat.select_one('.tweet-stat:nth-of-type(4) div.icon-container')
                        heart_count = heart_element.text.strip().replace(',', '') if heart_element.text.strip() else '0'
                                                
                        # Check if the 'icon-play' element exists
                        play_element = tweet_stat.select_one('.tweet-stat:nth-of-type(5) div.icon-container')
                        play_count = play_element.text.strip().replace(',', '') if play_element else '0'
                        
                        stats = {
                            'comments': int(comment_count),
                            'retweets': int(retweet_count),
                            'quotes': int(quote_count),
                            'likes': int(heart_count),
                            'plays': int(play_count)
                            }
                        
                        # Create a dictionary for each tweet
                        formatted_tweet = {
                            'fullname': fullname,
                            'username': username,
                            'text': text,
                            'link': link,
                            'date': formatted_date,
                            'stats': stats
                        }
                        formatted_tweets.append(formatted_tweet)
                                
                print(f"Scraped {len(formatted_tweets)} tweets for {key}")

                try:
                    next_cursor = soup.find('div', class_='show-more').find('a')
                    if next_cursor:
                        next_url = next_cursor['href']
                        self.url = f"https://nitter.poast.org{next_url}"
                    else:
                        print("No more next page. Scraping finished.")
                        break
                except AttributeError:
                    print("No more next page. Scraping finished.")
                    break
            
            date_to_json = datetime.now().strftime("%Y-%m-%d")
            save_to_json(formatted_tweets, f"{key}_{date_to_json}.json")
            
        driver.quit()