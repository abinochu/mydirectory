import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    links = parser.find_all('a', attrs={"class":"storylink"})
    td = parser.find_all('td', attrs={"class":"subtext"})
    for i in range(len(links)):
        new = {}
        author = td[i].find('a', attrs={"class":"hnuser"})
        new['author'] = author.contents[0]
        comments = td[i].find_all('a')[-1].contents[0]
        if comments == 'discuss':
            comments = 0
        else:
            comments = int(comments.split('\xa0')[0])
        new['comments'] = comments
        score = td[i].find('span', attrs={"class":"score"})
        new['points'] = int(score.contents[0].split(' ')[0])
        new['title'] = links[i].contents[0]
        new['url'] = links[i].get('href') 
        news_list.append(new)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    url = parser.find('a', attrs={"class":"morelink"}).get('href')
    return url


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

