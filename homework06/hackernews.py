from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string

@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    new = s.query(News).filter(News.id == request.query["id"]).first()
    new.label = request.query["label"]
    s.commit()
    
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    newsss = get_news('https://news.ycombinator.com/newest', 1)
    for new in newsss:
        print(new)
        auth = new.get('author')
        tit = new.get('title')
        print(tit, auth)
        ne = s.query(News).filter(News.author == auth).filter(News.title == tit).first()
        if ne is None:
            tmp = News(title=new['title'], 
                author=new['author'],
                url=new['url'],
                comments=new['comments'],
                points=new['points'])
            s.add(tmp)
            s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    bs = NaiveBayesClassifier(1)
    s = session()
    nolable = s.query(News).filter(News.label == None).all()
    X = processing(nolable)
    X_train = s.query(News).filter(News.label != None).all()
    y = []
    for item in X_train:
        y.append(item.label)
    X_train = processing(X_train)
    bs.fit(X_train, y)
    predictions = bs.predict(X)
    counter = 0
    for item in nolable:
        item.label = predictions[counter]
        counter += 1
    nolable.sort(key=lambda x: x.label)
    nolable.reverse()
    return template('news_template', rows=nolable)

def processing(data):
    titles = []
    translator = str.maketrans("", "", string.punctuation)
    for record in data:
        titles.append(record.title)
    prossessed_titles = []
    for title in titles:
        title.translate(translator)
        title = title.lower()
        title = title.split()
        prossessed_titles.append(title)
    #print(prossessed_titles)
    return prossessed_titles


if __name__ == "__main__":
    run(host="localhost", port=8080)