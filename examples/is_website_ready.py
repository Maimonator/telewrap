import requests
import time
import argparse

def main(url):
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            print("Success! The URL returned a 200 OK status code.")
            break
        else:
            print("The URL returned a status code of {}. Retrying in 5 seconds...".format(response.status_code))
            time.sleep(5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check if a URL returns a 200 OK status code')
    parser.add_argument('url', type=str, help='the URL to check')
    args = parser.parse_args()

    url = args.url
    main(url)
