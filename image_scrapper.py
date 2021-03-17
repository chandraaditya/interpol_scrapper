import json
import os

import filetype
import requests
import wget
from halo import Halo


def main():
    spinner = Halo(text='parsing json\n', spinner='dots')
    spinner.start()

    with open("results.json") as f:
        data = json.load(f)

    spinner.text = 'done parsing json\n'
    persons = data['persons']
    num_persons = len(persons)
    session = requests.Session()
    i = 1
    for person in persons:
        try:
            url = person['other']['_links']['images']['href']
            entity_id = person['other']['entity_id'].replace('/', '-')
            spinner.text = 'fetching ' + str(i) + '/' + str(num_persons) + '(' + str(
                round(((i / num_persons) * 100), 2)) + '%) ' + entity_id + '\n'
            data = session.get(url).json()
            i += 1
            for img_link in data['_embedded']['images']:
                l = img_link['_links']['self']['href']
                file = wget.download(l)
                kind = filetype.guess(file)
                if kind is None:
                    os.remove(file)
                else:
                    os.rename(file, 'images/' + entity_id + '-' + file + '.' + kind.extension)
        finally:
            continue
    spinner.stop()


if __name__ == "__main__":
    main()
