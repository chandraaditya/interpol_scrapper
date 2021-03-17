import json
import re
import timeit
import os
import filetype
import wget
import requests

from string import ascii_lowercase
from halo import Halo


def parseUrlName(name, gen, age, ageMax):
    return "https://ws-public.interpol.int/notices/v1/red?sexId=" + gen + "&ageMin=" + str(
        age) + "&ageMax=" + str(ageMax) + "&name=" + name + "&resultPerPage=160"


def parseUrlGender(gen, age, ageMax):
    return "https://ws-public.interpol.int/notices/v1/red?sexId=" + gen + "&ageMin=" + str(
        age) + "&ageMax=" + str(ageMax) + "&resultPerPage=160"


def parseUrlAge(age, ageMax):
    return "https://ws-public.interpol.int/notices/v1/red?ageMin=" + str(
        age) + "&ageMax=" + str(ageMax) + "&resultPerPage=160"


def scrap_images():
    spinner = Halo(text='parsing json\n', spinner='dots')
    spinner.start()

    with open("results.json") as f:
        data = json.load(f)

    spinner.text = 'done parsing json\n'
    persons = data['persons']
    num_persons = len(persons)

    try:
        os.mkdir('images')
    except:
        pass

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
                link = img_link['_links']['self']['href']
                file = wget.download(link)
                kind = filetype.guess(file)
                if kind is None:
                    os.remove(file)
                else:
                    os.rename(file, 'images/' + entity_id + '-' + file + '.' + kind.extension)
        finally:
            continue
    spinner.stop()


def main():
    spinner = Halo(text='fetching urls to parse\n', spinner='dots')
    spinner.start()

    source_code = "INTERPOL_RN"
    source_name = "INTERPOL Red Notices"
    source_url = "https://www.interpol.int/How-we-work/Notices/View-Red-Notices"

    session = requests.Session()

    html = session.get(source_url)
    html_string = html.text
    html.close()

    # country_id = list(filter(None, re.findall(r'<option value="(.+?)">', re.search(
    #     r'<select id="nationality" name="nationality" class="generalForm__selectArea">(\s+.+?)</select>',
    #     html_string).group(1))))
    #
    # country_list = list(filter(None, re.findall(r'">(.+?)</option>', re.search(
    #     r'<select id="nationality" name="nationality" class="generalForm__selectArea">(\s+.+?)</select>',
    #     html_string).group(1))))

    gender = list(filter(None, re.findall(r'value="(.?)"', re.search(
        r'<div class="generalForm__genderPick generalForm__radioButton">(\s+.+?)</div>', html_string).group(1))))

    init_url = "https://ws-public.interpol.int/notices/v1/red?resultPerPage=1"

    response = session.get(init_url)
    data = response.json()
    total_expected_results = data['total']
    response.close()

    total_fetched = 0

    start = timeit.default_timer()

    url_set = set()

    for age in range(0, 20):
        url = parseUrlAge(age, age)
        spinner.text = 'fetched ' + str(total_fetched) + '/' + str(total_expected_results) + '(' + str(
            round((total_fetched / total_expected_results) * 100, 2)) + '%), ' + url.replace(
            'https://ws-public.interpol.int/notices/v1/red?', '') + '\n'
        data = session.get(url).json()
        if data['total'] > 160:
            for gen in gender:
                url = parseUrlGender(gen, age, age)
                spinner.text = 'fetched ' + str(total_fetched) + '/' + str(total_expected_results) + '(' + str(
                    round((total_fetched / total_expected_results) * 100, 2)) + '%), ' + url.replace(
                    'https://ws-public.interpol.int/notices/v1/red?', '') + '\n'
                data = session.get(url).json()
                if data['total'] > 160:
                    for a in ascii_lowercase:
                        url = parseUrlName(a, gen, age, age)
                        spinner.text = 'fetched ' + str(total_fetched) + '/' + str(total_expected_results) + '(' + str(
                            round((total_fetched / total_expected_results) * 100,
                                  2)) + '%), ' + url.replace(
                            'https://ws-public.interpol.int/notices/v1/red?', '') + '\n'
                        data = session.get(url).json()
                        if data['total'] > 160:
                            for b in ascii_lowercase:
                                url = parseUrlName(a + b, gen, age, age)
                                spinner.text = 'fetched ' + str(total_fetched) + '/' + str(
                                    total_expected_results) + '(' + str(
                                    round((total_fetched / total_expected_results) * 100,
                                          2)) + '%), ' + url.replace(
                                    'https://ws-public.interpol.int/notices/v1/red?', '') + '\n'
                                data = session.get(url).json()
                                for u in data['_embedded']['notices']:
                                    if u['_links']['self']['href'] not in url_set:
                                        url_set.add(u['_links']['self']['href'])
                                        total_fetched += 1
                        else:
                            for u in data['_embedded']['notices']:
                                if u['_links']['self']['href'] not in url_set:
                                    url_set.add(u['_links']['self']['href'])
                                    total_fetched += 1
                else:
                    for u in data['_embedded']['notices']:
                        if u['_links']['self']['href'] not in url_set:
                            url_set.add(u['_links']['self']['href'])
                            total_fetched += 1
        else:
            for u in data['_embedded']['notices']:
                if u['_links']['self']['href'] not in url_set:
                    url_set.add(u['_links']['self']['href'])
                    total_fetched += 1

    data = {'source_code': source_code, 'source_name': source_name, 'source_url': source_url, 'persons': []}

    i = 1
    urls_len = len(url_set)

    for urls in url_set:
        spinner.text = 'fetching ' + urls.replace('https://ws-public.interpol.int/notices/v1/red/', '') + ' ' + str(
            i) + '/' + str(urls_len) + '(' + (str(round((i / urls_len) * 100, 2))) + '%)\n'

        p_data = session.get(urls).json()

        s_data = {'firstname': p_data['forename'], 'lastname': p_data['name'], 'about': {}}

        s_data['about']['date_of_birth'] = p_data['date_of_birth']
        s_data['about']['place_of_birth'] = p_data['place_of_birth']
        s_data['about']['nationality'] = p_data['nationalities']

        def switch(x):
            return {
                'M': 'Male',
                'F': 'Female',
                'U': 'Unknown'
            }[x]

        s_data['about']['gender'] = switch(p_data['sex_id'])

        s_data['other'] = {}
        s_data['other']['entity_id'] = p_data['entity_id']
        s_data['other']['languages_spoken_ids'] = p_data['languages_spoken_ids']
        s_data['other']['_embedded'] = p_data['_embedded']
        s_data['other']['_links'] = p_data['_links']

        s_data['other']['weight'] = p_data['weight']
        s_data['other']['height'] = p_data['height']
        s_data['other']['distinguishing_marks'] = p_data['distinguishing_marks']
        s_data['other']['eyes_colors_id'] = p_data['eyes_colors_id']
        s_data['other']['hairs_id'] = p_data['hairs_id']
        s_data['other']['arrest_warrants'] = p_data['arrest_warrants']

        data['persons'].append(s_data)
        i += 1

    spinner.text = 'writing to results.json'

    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    spinner.stop()

    scrap_images()

    stop = timeit.default_timer()

    print('Time: ', stop - start)
    print('Total queries processed ', len(data['persons']))


if __name__ == "__main__":
    main()
