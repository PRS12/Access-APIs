import xml.etree.ElementTree as ET
import json
import access_CPS
import access_LDP
import config


def download_full_articles(GUID):
    """
    Downloads and saves the entire content of the 50 most recent items about the provided GUID
    :param GUID: The GUID of a BBC entity - see BBC Things
    """
    request_json = access_LDP.get_creative_works_for_guid(GUID)
    urn_locators = access_LDP.extract_locators(request_json)
    print(urn_locators)
    content_results = access_CPS.get_content_by_locators(urn_locators)

    for counter, res in enumerate(content_results):
        filename = config.paths['full_articles_dir'] + str(counter) + '.txt'

        with open(filename, 'w') as writer:
            writer.write(json.dumps(res))


def download_article_text(GUID):
    """
    Downloads and saves the headline, shortHeadline, summary, and body text of the 50 most recent items about the provided GUID
    :param GUID: The GUID of a BBC entity - see BBC Things
    """
    request_json = access_LDP.get_creative_works_for_guid(GUID)
    urn_locators = access_LDP.extract_locators(request_json)
    print(urn_locators)
    content_results = access_CPS.get_content_by_locators(urn_locators)

    for counter, res in enumerate(content_results):
        print(res['headline'])
        print(res['shortHeadline'])
        print(res['summary'])
        body = text_from_body(res['body'])
        print(body)
        print('-----')
        filename = config.paths['plain_articles_dir'] + str(counter) + '.txt'

        with open(filename, 'w') as writer:
            writer.write(res['headline'] + '\n')
            writer.write(res['shortHeadline'] + '\n')
            writer.write(res['summary'] + '\n\n')
            writer.write(body)


# extract the plain text from the body element, in-built methods dont do a good enough job of ignoring metadata and
# HTML tags :/
def text_from_body(body_html):
    """
    Helper function to extract just the plain text from the HTML body element of news articles
    :param body_html: the body element of the HTML data for a news article
    :return: string of plain text extracted from HTML
    """

    def para_text(parent, string):
        for child in parent.findall('*'):  # behaviour of 'iter' would return itself and children at all depths
            if child.text:
                string += child.text
            string = para_text(child, string)
            if child.tail:
                string += child.tail
        return string

    root = ET.fromstring(body_html)
    text = ""
    for para in root.findall('{http://www.bbc.co.uk/asset}paragraph'):
        if para.text:
            text += para.text + para_text(para, "") + '\n'
        else:
            text += para_text(para, "") + '\n'

    return text


if __name__ == "__main__":
    # find GUIDs via BBC Things
    BREXIT_GUID = 'f94293fd-ff83-400e-8bc0-89ec01930fce'
    WORLD_CUP_GUID = '8819a847-defb-4b7f-a8f9-842a50ac9668'
    MUSK_GUID = 'bc0b91dc-0475-486a-95c5-3f47194dd1eb'
    GRENFELL_FIRE_GUID = 'dce810a0-6b42-4311-8035-8d8c19045d4d'
    GRENFELL_INQUIRY_GUID = 'f9b8e295-35b0-4dc4-b844-b62428c08b4e'

    download_article_text(BREXIT_GUID)
