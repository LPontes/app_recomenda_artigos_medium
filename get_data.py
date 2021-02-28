from datetime import date
from bs4 import BeautifulSoup
import requests as rq

def download_search_page(query, data):
    """ Obtém os dados dos artigos dos últimos 30 dias"""

    url = f'https://medium.com/{query}/archive/{str(data.year)}/{str(data.month).zfill(2)}/{str(data.day).zfill(2)}'
    page = rq.get(url)
   # soup = BeautifulSoup(page.text, 'html.parser')
    return page.text

def download_article_list(link):
    page = link
    soup = BeautifulSoup(page, 'html.parser')
    # stories are all articles found for that theme on the month
    stories = soup.find_all('div', class_='streamItem streamItem--postPreview js-streamItem')
    
    return stories


def parse_articles(story):

    dado = dict()

    author_box = story.find('div', class_='postMetaInline u-floatLeft u-sm-maxWidthFullWidth')
    author_url = author_box.find('a')['href']
        
    try:
        reading_time = author_box.find('span', class_='readingTime')['title']
    except:
        pass

    title = story.find('h3').text if story.find('h3') else '-'
    subtitle = story.find('h4').text if story.find('h4') else '-'

    if story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents'):
        claps = story.find('button', class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents').text 
    else:
        claps = 0

    if story.find('a', class_='button button--chromeless u-baseColor--buttonNormal'):
        responses = story.find('a', class_='button button--chromeless u-baseColor--buttonNormal').text
    else:
        responses = '0 responses'

    reading_time = reading_time.split()[0]
    responses = responses.split()[0]

    story_url = story.find('a', class_='button button--smaller button--chromeless u-baseColor--buttonNormal')['href']  

    dado['reading_time'] = reading_time
    dado['title'] = title
    dado['claps'] = claps
    dado['responses'] = responses
    dado['link'] = story_url

    return dado