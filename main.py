import argparse

from lib.twitter_poast import TwitterPost

def parse_args():
    parser = argparse.ArgumentParser(description="Twitter Scraper")
    parser.add_argument("--key", type=str, help="Search keyword", required=True)
    parser.add_argument("--start_date", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end_date", type=str, help="End date (YYYY-MM-DD)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    url = "https://nitter.poast.org"
    TwitterPost(url).run_scraper(args.key, args.start_date, args.end_date)
    