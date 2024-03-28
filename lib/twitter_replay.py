import os
import sys
import platform
import time
from datetime import datetime
from selenium import webdriver
from fake_headers import Headers
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup

from .data_extract import DataExtract
from lib.utils import save_to_json

class TwitterReplay:
    def __init__(self):
        self.url = None
        self.driver = None
        
    def run_scraper_profiel(self, url: str) -> None:
        
        try:
            self.driver = self.initialize_driver()
            time.sleep(5)
            
            tweet_replay = []
            for link in url:
                while link:
                    self.driver.get(link)
                    time.sleep(5)
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    replay = soup.find("div", {"class": "timeline-item thread-last "})
                
                    for replays in replay:
                        fullname = DataExtract.fullname(replays)
                        username = DataExtract.username(replays)
                        text = DataExtract.text(replays)
                        hashtag = DataExtract.hashtag(replays)
                        date = datetime.strptime(DataExtract.date(replays), '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')
                        link = DataExtract.link(replays)
                        media = DataExtract.media(replays)
                        stats = DataExtract.stats(replays)
                        
                        # Jika tidak ada hashtag, tetapkan nilai list kosong
                        if not hashtag:
                            hashtag = []
                            
                        # Perbaiki representasi media
                        # Jika ada media, ubah representasi menjadi list
                        if isinstance(media, str):
                            media = [media]
                            
                        # Buat dictionary untuk setiap tweet
                        replay = {
                            "type" : "replay",
                            "fullname": fullname,
                            "username": username,
                            "text": text,
                            "hashtag": hashtag,
                            "date": date,
                            "link": link,
                            "media": media,
                            "stats": stats
                        }
                        
                        tweet_replay.append(replay)
                        
                    print(f"Scraped {len(tweet_replay)} tweets")
                    
                    try:
                        next_cursor = soup.find('div', class_='show-more').find('a')
                        if next_cursor:
                            next_url = next_cursor['href']
                            self.url = f"https://nitter.poast.org{next_url}"
                            time.sleep(5)
                        else:
                            print("No more next page. Scraping finished.")
                            break
                    except AttributeError:
                        print("No more next page. Scraping finished.")
                        
                date = datetime.strptime(DataExtract.date(replays), '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S')
                save_to_json(tweet_replay, f"{date}.json")
                          
            return tweet_replay
        except WebDriverException as e:
            print(f"Error: {e}")