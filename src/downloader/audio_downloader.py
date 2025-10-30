import requests
import logging
import time

def download_file(url, filename, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                file.write(response.content)
            logging.info(f"Downloaded: {filename}")
            return True
        except requests.RequestException:
            attempt += 1
            if attempt < retries:
                time.sleep(2 ** attempt)
            else:
                logging.error(f"Failed: {url}")
    return False
