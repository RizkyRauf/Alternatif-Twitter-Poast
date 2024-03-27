# lib/fiild_data_extract.py
import unicodedata
from datetime import datetime

class DataExtract:
    """
    Kelas bertanggung jawab untuk mengikis pos Twitter.
    """
    @staticmethod
    def fullname(tweet):
        try:
            fullname = unicodedata.normalize('NFKD', tweet.find('a', class_='fullname').text).encode('ascii', 'ignore').decode('utf-8')
            return fullname
        except:
            return '-'
        
    @staticmethod
    def username(tweet):
        try:
            username = unicodedata.normalize('NFKD', tweet.find('a', class_='username').text).encode('ascii', 'ignore').decode('utf-8')
            return username
        except:
            return '-'
        
    @staticmethod
    def text(tweet):
        try:
            text = unicodedata.normalize('NFKD', tweet.find('div', class_='tweet-content media-body').text.strip()).encode('ascii', 'ignore').decode('utf-8')
            return text
        except:
            return '-'
        
    @staticmethod
    def date(tweet):
        try:
            date_element = tweet.find('span', class_='tweet-date').find('a') 
            date_text = date_element['title'] if date_element else ''
            formatted_date = datetime.strptime(date_text, '%b %d, %Y \u00b7 %I:%M %p UTC').strftime('%d/%m/%Y %H:%M:%S') if date_text else ''
            return formatted_date
        except:
            datenow = datetime.strptime(datetime.now().strftime('%d/%m/%Y %H:%M:%S'), '%d/%m/%Y %H:%M:%S')
            return datenow
   
    @staticmethod
    def link(tweet):
        try:
            link = tweet.find('a', class_='tweet-link')['href'].replace('#m', '') if tweet.find('a', class_='tweet-link') else ''
            link = f"https://twitter.com{link}"
            return link
        except:
            return '-'
        
    @staticmethod
    def hashtag(text):
        try:
            hastags = [tag.strip("#") for tag in text.split() if tag.startswith("#")]
            return hastags
        except:
            return None
        
    @staticmethod
    def media(tweet):
        try:
            image_urls = []
            attachments = tweet.find_all('div', class_='attachment image')
            for attachment in attachments:
                image_url = attachment.find('a', class_='still-image')['href']
                image_url = f"https://nitter.poast.org{image_url}"
                image_urls.append(image_url)
                
            video_urls = []
            attachments = tweet.find_all('div', class_='attachment video-container')
            for attachment in attachments:
                video_url = attachment.find('source')['src']
                video_urls.append(video_url)
                
            media_urls = {'images': image_urls, 'videos': video_urls}
            return media_urls
        except:
            return {'images': [], 'videos': []}
        
    @staticmethod
    def stats(tweet):
        try:
            stats = {}
            tweet_stat = tweet.find('div', class_='tweet-stats')
            if tweet_stat:
                # Check if the 'icon-comment' element exists
                comment_element = tweet_stat.select_one('.tweet-stat:nth-of-type(1) div.icon-container')
                comment_count = comment_element.text.strip().replace(',', '') if comment_element else '0'
                
                # Check if the 'retweet' element exists
                retweet_element = tweet_stat.select_one('.tweet-stat:nth-of-type(2) div.icon-container')
                retweet_count = retweet_element.text.strip().replace(',', '') if retweet_element else '0'
                
                # Check if the 'icon-quote' element exists
                quote_element = tweet_stat.select_one('.tweet-stat:nth-of-type(3) div.icon-container')
                quote_count = quote_element.text.strip().replace(',', '') if quote_element else '0'
                
                # Check if the 'icon-heart' element exists
                heart_element = tweet_stat.select_one('.tweet-stat:nth-of-type(4) div.icon-container')
                heart_count = heart_element.text.strip().replace(',', '') if heart_element else '0'
                
                # Convert counts to integers
                comment_count = int(comment_count) if comment_count else 0 
                retweet_count = int(retweet_count) if retweet_count else 0 
                quote_count = int(quote_count) if quote_count else 0 
                heart_count = int(heart_count) if heart_count else 0
                
                stats = {
                    'comments': comment_count,
                    'retweets': retweet_count,
                    'quotes': quote_count,
                    'likes': heart_count
                }                
                return stats
        except AttributeError:
            return {}
                