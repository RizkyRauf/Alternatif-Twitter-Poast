from lib.twitter_poast import TwitterPost

if __name__ == "__main__":
    url = "https://nitter.poast.org"
    TwitterPost(url).run_scraper()