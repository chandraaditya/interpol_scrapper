import requests


def main():
    firstname = 'ATIKAT'
    lastname = 'KURBANOVA'
    query = '{"query":{"multi_match":{"query":"' + firstname + ' ' + lastname + '","type":"cross_fields","fields":["firstname","lastname"],"operator":"and"}}}'
    header = {'Content-Type': 'application/json'}
    response = requests.get('http://localhost:9200/bad_people/doc/_search', data=query, headers=header).json()
    print(response)


if __name__ == "__main__":
    main()
