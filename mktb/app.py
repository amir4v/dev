import time
import requests as r
from bs4 import BeautifulSoup as bs
from urls import urls as get_urls
from cookies import cookies
from dl import download
from until import write_where


def do():
    index, urls = get_urls()
    
    if len(urls) == 0:
            print('[urls] list is Empty.')
            exit(0)
    
    for url in urls:
        html = r.get(url, cookies=cookies).text

        soup = bs(html, features="html.parser")
        a_tags = soup.find_all("a")

        for a in a_tags:
            href = a.get('href')
            if href and href.endswith('.mp4') and 'hq' in href:
                
                filename = href.split('&name=')[1]
                print('...Start downloading...', filename)
                print(href)
                
                completed, filename = download(href)
                if completed:
                    write_where(index)
                    print('[COMPLETED]', filename, end='\n\n\n')
                else:
                    return False
        
        index += 1


while True:
    try:
        do()
    except Exception as e:
        print('[Exception]', 'time.sleep', e)
        time.sleep(5)
        pass