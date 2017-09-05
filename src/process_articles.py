
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import glob
import pickle
import datetime
import requests
import json
import api_keys

file_list = glob.glob("../data/raw_articles/*.txt")
sid = SentimentIntensityAnalyzer()

def get_valid_preceeding_date(finance_data, date_published):
    for i in range(5):
        try:
            return finance_data['Time Series (Daily)'][(date_published - datetime.timedelta(days=i)).strftime("%Y-%m-%d")]
        except KeyError:
            continue

    raise Exception('Preceeding date for', date_published, 'not found.')


def get_valid_current_date(finance_data, date_published):
    for i in range(5):
        try:
            return finance_data['Time Series (Daily)'][(date_published + datetime.timedelta(days=(i+1))).strftime("%Y-%m-%d")]
        except KeyError:
            continue

    raise Exception('After date for', date_published, 'not found.')

def get_article_finance_data(symbol, publish_date):
    resp_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&apikey=' + api_keys.get_alpha_api_key() + '&outputsize=full'
    req = requests.request('GET', resp_url)
    finance_data = json.loads(req.content)

    previous_data_date = get_valid_preceeding_date(finance_data, publish_date)
    current_data_date = get_valid_current_date(finance_data, publish_date)

    return (float(previous_data_date['4. close']), float(current_data_date['4. close']))

data_arr = []

for company_file in file_list:
    print(company_file)

    with open(company_file, 'rb') as f:
        articles_array = pickle.load(f)

        for article in articles_array:
            count = 0
            pos_count = 0
            neg_count = 0
            pos_compound = 0
            neg_compound = 0
            processed_sentence = True

            try:
                for sentence in article[3].split('.'):
                    count += 1
                    scores = sid.polarity_scores(sentence)
                    if scores['pos'] > scores['neg']:
                        pos_count += 1
                        pos_compound += scores['compound']
                    elif scores['neg'] > scores['pos']:
                        neg_count += 1
                        neg_compound += scores['compound']

                if pos_count > 0:
                    pos_compound /= pos_count

                if neg_count > 0:
                    neg_compound /= neg_count
            except AttributeError:
                processed_sentence = False

            if processed_sentence:
                sent_data_tuple = (pos_count, neg_count, pos_compound, neg_compound)
                publish_date = datetime.datetime.strptime(article[2], '%d/%m/%Y %H:%M:%S')
                try:
                    article_finance_data = get_article_finance_data(article[0], publish_date)
                    data_tuple = sent_data_tuple + article_finance_data
                    data_arr.append(data_tuple)
                    print(data_tuple, len(data_arr))
                except json.JSONDecodeError:
                    print("Encountered a JSON decoding error.", sent_data_tuple, publish_date, company_file, article)

with open('../data/processed_statements.txt', 'wb') as f:
    pickle.dump(data_arr, f)