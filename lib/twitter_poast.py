
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

class TwitterPost:
    """
    Kelas bertanggung jawab untuk berinteraksi dengan pos Twitter.

    Metode:
        configure_browser_options: Mengonfigurasi opsi browser untuk Selenium.
        initialize_driver: Menginisialisasi driver Selenium.
        run_scraper: Menjalankan pengikis Twitter.
    """
    def __init__(self, url):
        """
        Inisialisasi TwitterPost dengan URL.
        """
        self.url = url

    def configure_browser_options(self):
        """
        Mengonfigurasi opsi browser untuk Selenium.

        Returns:
            options: Opsi browser untuk Selenium.
        """
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-notifications')
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            return options
        
        except Exception as e:
            print(f"Error initializing driver : {e}")
            raise
    
    def initialize_driver(self):
        """
        Menginisialisasi driver Selenium.

        Returns:
            driver: Driver Selenium yang diinisialisasi.
        """
        try:
            chrome_driver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../driver/chromedriver.exe"))
            options = self.configure_browser_options()
            service = ChromeService(executable_path=chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            return driver

        except Exception as e:
            print(f"Error initializing driver : {e}")
            raise Exception
    
    def run_scraper(self):
        """
        Menjalankan pengikis Twitter.
        """
        from lib.scraper import Scraper
        path_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib/list_keywords.txt"))
        key = input("Search Keyword: ")
        scraper = Scraper(self.url, path_file)
        scraper.scrape_tweets(key)