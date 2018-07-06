import requests
import config

# CPS batch API guide
# https://confluence.dev.bbc.co.uk/display/cps/Batch+Service


def get_content_by_locators(item_locators):
    """
    Given a list of URN item locators, return the content of each item
    :param item_locators: a list of URN item locators
    :return: a json dict of the content of each URN passed into the function
    """

    assets_string = ''
    for locator in item_locators:
        assets_string += '&curie=asset:' + locator
    assets_string = assets_string[1:]

    # ignore verifying the SSL certificate server side with verify=False
    headers = {'Accept': 'application/json',
               'X-Candy-Audience': 'Domestic',
               'X-Candy-Platform': 'Desktop'}

    print('Collecting data...')
    req = requests.get('https://content-api-ext-a127.api.bbci.co.uk/batch?' + assets_string +
                       '&api_key=' + config.keys['API_KEY_CPS_EXT'],
                       cert=(config.paths['pem'], config.paths['key']),
                       verify=False, headers=headers)
    return req.json()['results']
