# This file populates the /data/ folder with all recent news that

import requests
import json
import pickle
import os

def create_company_crosswalk():
    with open("../data/company_list.txt") as file:
        data = file.read()

    company_crosswalk = [item.split('\t') for item in data.split('\n')]
    return company_crosswalk

def get_news_response(company_id):
    req = requests.request('GET', 'http://myallies.com/api/news/' + company_id)
    if req.status_code != 200:
        return []

    article_data = json.loads(req.content)

    id_arr = []
    for row in article_data:
        id_arr.append(row['NewsID'])

    return id_arr

def get_articles_from_ids(id_arr, existing_id_arr):
    details_array = []
    for article_id in id_arr:
        if (existing_id_arr == None) or (existing_id_arr != None and article_id not in existing_id_arr):
            req = requests.request('GET', 'http://myallies.com/api/newsitem/' + str(article_id))
            article_data = json.loads(req.content)
            details_array.append((article_id, article_data['PublishDate'], article_data['Content']))

    return details_array

crosswalk = create_company_crosswalk()

for symbol, name in crosswalk:
    print(symbol, name)
    target_file = '../data/raw_articles/Articles_' + name.replace(' ', '_') + '.txt'
    article_id_array = get_news_response(symbol)

    if os.path.exists(target_file) and os.path.getsize(target_file) > 4:
        with open(target_file, 'rb') as f:
            existing_list = pickle.load(f)
            article_array = existing_list + get_articles_from_ids(article_id_array, [article[0] for article in existing_list])
    else:
        article_array = get_articles_from_ids(article_id_array, None)

    if len(article_array) > 0:
        with open(target_file, 'wb') as f:
            pickle.dump(article_array, f)