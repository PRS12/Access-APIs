import requests
import config
from fuzzywuzzy import fuzz
import xml.etree.ElementTree as ET

# https://monitoring.bbc.co.uk/api


def get_bio(search_text):
    """
    Get the summary text about a person who has an entry in BBC Monitoring
    :param search_text: Search text as 'Firstname Surname' - somewhat tolerant to typos
    :return: extracted bio about the person as a string
    """

    payload = {"username": config.keys['BBC_username'], "password": config.keys['BBC_password']}

    with requests.Session() as s:
        s.post('https://monitoring.bbc.co.uk/api/v0/login', json=payload,
               headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

        search_results = s.get("https://monitoring.bbc.co.uk/api/v0/search?searchText=" + search_text +
                               "&category=BIOGRAPHY&limit=20&sort=publication_time&sortDirection=DESC",
                               headers={'Accept': 'application/json'})

        search_results = search_results.json()['products']

        # surnames may have multiple parts, hence you dont want to do a simple string split
        space = search_text.index(' ')
        search_name = search_text[space+1:] + ', ' + search_text[:space]

        search_id = False

        for result in search_results:
            # tokenize and lowercase comparison
            if fuzz.token_set_ratio(search_name, result['headline']) > 80:
                # print(result)
                search_id = result['id']

        # First see if the person has a bio
        if search_id:
            search_content = s.get("https://monitoring.bbc.co.uk/api/v0/product/" + search_id,
                                   headers={'Accept': 'application/json'})
            # print(search_content.json()['bodyHtml'])
            summary = extract_bio_text(search_content.json()['bodyHtml'])
            return summary
        # If they do not, see if they are a member of the government
        else:
            gov_list = get_government_list()

            for gov_person in gov_list.keys():
                # tokenize and lowercase comparison
                if fuzz.token_set_ratio(search_name, gov_person) > 80:
                    return gov_list[gov_person]

        return ""


def extract_bio_text(html_result):
    """
    Extract the summary text from a string of HTML
    :param html_result: HTML string containing a summary about an entity
    :return: summary string
    """

    root = ET.fromstring(html_result)
    # selection of the summary section from anywhere relative to the root, and the 'para' grandchild element of this
    summary_section = root.find(".//section[@class='summary']*/div[@class='para']")

    return summary_section.text


def get_government_list():
    """
    Many members of government do not have dedicated MonRes entries - this function extracts data about current members of governemt to expand the utility of retriving bios
    :return: dict of members of government and the posts they hold
    """

    payload = {"username": config.keys['BBC_username'], "password": config.keys['BBC_password']}

    with requests.Session() as s:
        s.post('https://monitoring.bbc.co.uk/api/v0/login', json=payload,
               headers={'Accept': 'application/json', 'Content-Type': 'application/json'})

        gov_list_html = s.get("https://monitoring.bbc.co.uk/api/v0/product/" + '3227409',
                              headers={'Accept': 'application/json'})

        gov_list_html = gov_list_html.json()['bodyHtml']

    root = ET.fromstring(gov_list_html)
    posts = root.findall(".//section[@class='group']*/div[@class='post']")
    posts_dict = {}

    for post in posts:
        post_name = post.find("*/span[@class='main']")
        person_name = post.find("*//span[@class='keyname']").text
        person_name += post.find("*//span[@class='othername']").text
        posts_dict[person_name] = post_name.text

    return posts_dict


def get_wiki_bio(search_term):
    """
    Get the summary about a person from WikiData - useful default for people without MonRes entries.
    :param search_term: Name of the person to be searched
    :return: extracted bio about the person as a string
    """
    req = requests.get('https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&'
                       'search=' + search_term + '&language=en')

    res = req.json()['search'][0]
    searchID = res['title']
    req2 = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&format=json'
                        '&ids=' + searchID)

    searchInfo = req2.json()['entities'][searchID]

    return searchInfo['descriptions']['en']['value']


if __name__ == "__main__":
    x = get_bio('Angela Merkel')
    print(x)
