import requests


def get_articles(query='', section='', publication_time='', start=''):
    """
    Get the 10 most recent news/sports articles about a given query
    :param query: search terms to use
    :param section: specific news section to use
    :param publication_time: leave blank or use one of: today, thisweek, thismonth, thisyear
    :param start: Results are given in pages of 10, use start=10, 20 etc. to get more/older results
    :return: json structure of search results including title, synopsis, tags, section, urn, url
    """

    # returns the top 10 results (assuming they exist, to get more results use start=10 for example
    # the documented 'rows' parameter does not seem to work in reality
    req = requests.get('https://dlpszmh6jdkfv.cloudfront.net/search-api?&lang=en&tags=true' +
                       '&published=' + publication_time +
                       '&has_url=true&media_type=text&category_site=news,sport' +
                       '&section=' + section +
                       '&start=' + start +
                       '&q=' + query)

    # if the extracted section does not exist, use it just as a general query
    if not req.json()['results'] and section != '':
        if not query:
            query = section
        req = requests.get('https://dlpszmh6jdkfv.cloudfront.net/search-api?&lang=en&tags=true' +
                           '&published=' + publication_time +
                           '&has_url=true&media_type=text&category_site=news,sport' +
                           '&section=' + '' +
                           '&q=' + query)

    return req.json()['results']


if __name__ == "__main__":
    articles = get_articles(section='london', publication_time='thisweek')
    for art in articles:
        print(art['title'], '\t\t', art['synopsis'])

# 'titles' gives a dict of different titles such as 'full'\
# 'content' tag only gives the first sentence or so depending on its length

# noticeable difference between query=X and section=X
# query=... gives info about X in the world, whereas section=... gives news happening IN that place

# and the 'tag' parameter just does not seem to be implemented as described \_(ツ)_/¯
