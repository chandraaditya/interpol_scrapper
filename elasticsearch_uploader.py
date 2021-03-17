import json

from elasticsearch import Elasticsearch


def main():
    es = Elasticsearch(
        ['localhost'],
        port=9200
    )

    with open('results.json', 'r') as f:
        data = json.load(f)

    i = 0

    for person in data['persons']:
        persons_str = json.dumps(person)
        print(persons_str)
        es.index(index='bad_people', doc_type='doc', id=i, body=persons_str)
        i = i + 1


if __name__ == "__main__":
    main()
