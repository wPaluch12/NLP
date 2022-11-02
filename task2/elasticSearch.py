import json
from os import listdir
import requests


# curl -X PUT "localhost:9200/pjntry?pretty" -H "Content-Type: application/json" -d'
# {
# "settings": {
#   "analysis": {
#     "filter": {
#         "pjn_synonyms": {
#              "type": "synonym",
#              "synonyms": [
#                  "kpc, kodeks postępować cywilny",
#                  "kpk, kodeks postępować karny",
#                  "kk, kodeks karny",
#                  "kc, kodeks cywilny"
#              ]
#         }
#     },
#     "analyzer": {
#        "pjn_analyzer": {
#            "type": "custom",
#            "tokenizer": "standard",
#            "filter": [
#                "lowercase",
#                "morfologik_stem",
#                "pjn_synonyms"
#           ]
#        }
#     }
#   }
# },
# "mappings": {
#   "properties": {
#     "content": {
#       "type": "text",
#       "analyzer": "pjn_analyzer",
#       "search_analyzer": "pjn_analyzer"
#     },
# "title": {
#       "type": "text"
#     }
#   }
# }
# }
# '


def load_data():
    num = 0
    for file in listdir("../ustawy"):
        with open(f'../ustawy/{file}', "r", encoding='utf-8') as f:
            num += 1
            data = f.read()
            data = {"content": data, "title": file}
            response = requests.post(f"http://localhost:9200/pjntry/_doc/{num}", headers={"Content-Type": "application/json"},json=data)
            if response.status_code != 200:
                print(json.loads(response.content))


def get_response(query_file,elastic_url):
    with open(query_file, "r", encoding='utf-8') as f:
        query = json.loads(f.read())
    headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
    response = json.loads(requests.get(elastic_url, json=query, auth=('elastic', 'XTCeiO8mlhavlnHFW-6+'), verify=False, headers=headers).content)
    return response #['hits']['total']['value']


if __name__ == '__main__':

    # #task5
    # load_data()

    #task 6 Determine the number of legislative acts containing the word ustawa (in any form).
    file = "search_query.json"
    url = 'http://localhost:9200/pjntry/_search'
    resp = get_response(file,url)['hits']['total']['value']
    print(f'total files that include word ustawa: {resp}')

    # #task 7 Determine the number of occurrences of the word ustawa by searching for this particular form, including the other inflectional forms.
    # file = "task7.json"
    # url = 'http://localhost:9200/pjntry/_termvectors'
    # resp = get_response(file, url)['term_vectors']['content']['terms']['ustawa']['ttf']
    # print(f'All occurences of word ustawa: {resp}')
    # # #24934

    # # task 8 Determine the number of occurrences of the word ustaw by searching for this particular form, including the other inflectional forms.
    # file = "task8.json"
    # url = 'http://localhost:9200/pjntry/_termvectors'
    # resp = get_response(file, url)
    # total = resp['term_vectors']['content']['terms']['ustawa']['ttf'] + resp['term_vectors']['content']['terms']['ustawić']['ttf']
    # print(f'All occurences {total}')
    # # # 24934+913

    # # task 9 Determine the number of legislative acts containing the words kodeks postępowania cywilnego in the specified order, but in any inflection form.
    # file = "task9.json"
    # url = 'http://localhost:9200/pjntry/_search'
    # resp = get_response(file, url)['hits']['total']['value']
    # print(f'All occurences {resp}')
    # # 99

    # # task 10 Determine the number of legislative acts containing the words wchodzi w życie (in any form) allowing for up to 2 additional words in the searched phrase.
    # file = "task10.json"
    # url = 'http://localhost:9200/pjntry/_search'
    # resp = get_response(file, url)['hits']['total']['value']
    # print(f' {resp}')
    # # 1174

    # #task 11 Determine the 10 documents that are the most relevant for the phrase konstytucja.
    # file = "task11.json"
    # url = 'http://localhost:9200/pjntry/_search'
    # resp = get_response(file, url)
    # docs =[element['_source']['title'] for element in resp['hits']['hits']]
    # print(f'Most relevant: {docs}') #
    # #['1997_629.txt', '2000_443.txt', '1997_604.txt', '1996_350.txt', '1997_642.txt', '2001_23.txt', '1996_199.txt', '1999_688.txt', '2001_1082.txt', '1997_681.txt']

    # #task 12 Print the excerpts containing the word konstytucja (up to three excerpts per document) from the previous task.
    # file = "task12.json"
    # url = 'http://localhost:9200/pjntry/_search'
    # print(f' {get_response(file, url)}')  # ['hits']['hits']

