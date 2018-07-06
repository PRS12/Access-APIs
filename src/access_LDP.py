import requests
import config

# LDP API guide
# https://ldp-core.api.bbci.co.uk/ldp-core/


def get_creative_works_for_guid(item_guid, page=1):
    """
    Download creative works from LDP for a given GUID. Search for the desired GUID on BBC Things
    :param item_guid: The unique GUID corresponding to the entity to be found
    :param page: Results are split into pages of 50 items, get the first page by default
    :return: Returns a json dict of creative works
    """

    # ignore verifying the SSL certificate server side with verify=False
    headers = {'Accept': 'application/ld+json'}
    req = requests.get('https://ldp-core.api.bbci.co.uk/ldp-core/creative-works-v2?about=' + item_guid +
                       '&type=NewsItem'
                       '&api_key=' + config.keys['API_KEY_LDP'] + '&page-size=50' +
                       '&page=' + str(page),
                       cert=(config.paths['pem'], config.paths['key']),
                       verify=False, headers=headers)
    return req.json()['results']


def extract_urn_locators(creative_works):
    """
    Given a list of creative works, extract the URN item locators so that their content can be downloaded via LDP
    :param creative_works: A list of creative works
    :return: A list of URN locators
    """
    locators = []
    for item in creative_works:
        locator = item['locator'][0]  # Select the urn asset
        locators += [locator[10:]]  # ignore the start 'urn:asset:'
    return locators
