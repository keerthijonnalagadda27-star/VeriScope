import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def scrape_article(url:str)->dict:
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response=requests.get(url,headers=headers,timeout=10)

        response.raise_for_status()


        # raise_for_status() throws an error if response code is 4xx or 5xx
        # e.g. 404 Not Found, 403 Forbidden — catches bad URLs early

        soup=BeautifulSoup(response.content,'html.parser')

        title_tag=soup.find('h1')

        title=title_tag.get_text(strip=True) if title_tag else ''


        #get text aa html tags remove chesi text isthundi and strip=true ante mundu venaka extra trailing spaces lekapothe chey amd if no h1 found,return empty string

        paragraphs=soup.find_all('p')

        body=' '.join([p.get_text(strip=True) for p in paragraphs])
        #vachina paragraphs anni with space b/w them ichi join chestundi as a list

        full_text=f"{title} {body}"

        domain=urlparse(url).netloc

        return {
            "text": full_text,
            "title": title,
            "domain": domain,
            "success": True
        }

    except Exception as e:
        return {
            "text":"",
            "title":"",
            "domain":"",
            "success":False,
            "error":str(e)
        } 
    




