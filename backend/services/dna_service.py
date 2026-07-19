import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

NEWS_API_KEY=os.getenv("NEWS_API_KEY")

def search_similar_articles(query:str)->list:
    try:
        search_query=query[:100]
        #ante news api works better with short queries so oorike 100 chars teeksunnam
        url="https://newsapi.org/v2/everything"
        params={
            "q":search_query,
            "apiKey":NEWS_API_KEY,
            "sortBy":"publishedAt",
            "pageSize":20,
            "language":"en"
        }
        response=requests.get(url,params=params,timeout=10)
        response.raise_for_status()
        data=response.json()

        #ee data lo mana requests elago downloads the webpage kabatti aa text untadi...adi json lo unchi manam netx work cheskuntam

        # first manam news api manaki em send chestundi anna aah strcuture meeda idea undali.. example ki 
        # {
#     "status": "ok",
#     "articles": [
#         {
#             "title": "AI News",
#             "url": "https://www.bbc.com/news/123",
#             "publishedAt": "2026-06-28",
#             "source": {
#                 "name": "BBC"
#             }
#         },
#         {
#             "title": "Sports",
#             "url": None,
#             "publishedAt": "2026-06-27"
#         }
#     ]
# }

        articles=[]
        for article in data.get("articles",[]):
            if not article.get("url") or not article.get("publishedAt"):
                continue

            domain=urlparse(article["url"]).netloc

            articles.append({
                "title": article.get("title", ""),
                "url": article["url"],
                "domain": domain,
                "published_at": article["publishedAt"],
                "source": article["source"]["name"]
            })

        articles.sort(key=lambda x: x["published_at"])
        return articles
        
        # sort by published_at — earliest first
        # ante early ga unna article is assumed kadha to be published 1 st ani so...

    except Exception as e:
        print(f"NewsAPI error:{str(e)}")
        return []
    

def call_java_dsa(articles:list)->dict:
    JAVA_SERVICE_URL=os.getenv("JAVA_SERVICE_URL", "http://localhost:8002")
    try:
        response=requests.post(
            f"{JAVA_SERVICE_URL}/dsa/spread",
            json={"articles":articles},
            timeout=5
        )
        if response.status_code==200:
            return response.json()
        return {"nodes":[],"edges":[],"spread_path":[],"origin":None}
    except Exception as e:
        print(f"DSA service is unavailable:{e}")
        return {"nodes":[],"edges":[],"spread_path":[],"origin":None}
    
def get_source_dna(text:str)->dict:
    #idi mana main fxn..manam text isthe daani batti similar articles and vati gurinchi trace chestundi
    articles=search_similar_articles(text)

    if not articles:
        return {
            "dna_available":False,
            "message":"No related articles found",
            "articles":[],
            "graph":None
        }
    graph_data=call_java_dsa(articles)

    return{
        "dna_available":True,
        "total_sources":len(articles),
        "origin":graph_data.get("origin"),
        "spread_path":graph_data.get("spread_path",[]),
        "graph": {
            "nodes":graph_data.get("nodes",[]),
            "edges":graph_data.get("edges",[])
        },
        "articles":articles[:10]
        # idi mana top 10 articles ni isthundi

    }    

