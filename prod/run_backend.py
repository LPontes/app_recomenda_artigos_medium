from get_data import *
from ml_utils import *
import datetime
import time

queries = [ 'python' , 'data-science']

def update_db():
    with open("novos_artigos.json", 'w+') as output:
        for query in queries:
            
            for i in range(5):
                data = datetime.date.today() - datetime.timedelta(days = i)
                print(query, data)
                search_page = download_search_page(query, data)
                article_list = download_article_list(search_page)

                for story in article_list:
                    artigo = parse_articles(story)
                    p = compute_prediction(artigo)

                    data_front = {"title": artigo['title'], "score": float(p), "link": artigo['link']}
                    data_front['update_time'] = time.time_ns()

                    print(artigo['link'], json.dumps(data_front))
                    output.write("{}\n".format(json.dumps(data_front)))
    return True