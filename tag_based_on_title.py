import pywikibot
import requests

# The name space to retrieve pages from
# https://www.mediawiki.org/wiki/Manual:Namespace#Built-in_namespaces to see available namespaces
NAMESPACE = 6
# Number of pages to extract at a time; used in get_pages_json() in params for "aplimit"
PAGES_LIMIT = 2


def get_api_url() -> str:
    """
    Retrieves the API URL of the wiki

    :return: string of the path to the API URL of the wiki
    """

    site = pywikibot.Site()
    url = site.protocol() + "://" + site.hostname() + site.apipath()
    return url


def get_pages_json(url, continue_from="") -> "Page Generator":
    """
    Retrieves a Page Generator with all the pages to be scanned

    :param url: string of the path to the API URL of the wiki
    :param continue_from: string of page title to continue from; defaults to beginning of wiki
    :return: a list of page titles
    """

    # Retrieving the pages to sort
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "list": "allpages",
        "apcontinue": continue_from,
        "apnamespace": NAMESPACE,
        "aplimit": PAGES_LIMIT
    }

    session = requests.Session()
    request = session.get(url=url, params=params, verify=False)
    pages_json = request.json()

    return pages_json


def get_categories(title: str) -> []:
    """
    Gets an array of the category names based on the parameter title

    :param title: page title to be analyzed
    :return: array of strings
    """

    categories = []

    if any(word in title for word in ["Memo", "memo"]):
        categories.append("Memos")
    if any(word in title for word in ["Interview", "interview"]):
        categories.append("Interviews")
    if any(word in title for word in ["Agenda", "agenda"]):
        categories.append("Agendas")
    if any(word in title for word in ["Letter", "letter"]):
        categories.append("Letters")
    if any(word in title for word in ["Guide", "guide"]):
        categories.append("Guides")

    return categories


def add_category(title, category) -> None:
    """
    Adds the parameter category to the parameter page

    :param title: page title to be modified
    :param category: category to be added to the page
    :return: None
    """

    site = pywikibot.Site()

    page = pywikibot.Page(site, title)
    page_text = page.text

    if page_text.find(category) == -1:
        print("'%s' not in '%s'... Adding" % (category, page))
        page_text = u'\n'.join((page_text, category))
        page.text = page_text
        page.save(u"Tagged with: " + category, botflag=True)
    else:
        print("'%s' already in '%s'... Skipping." % (category, page))


def main() -> None:
    """
    Driver. Retrieves all pages in NAMESPACE and scans their titles to find categories to add. Proceeds to tag the
    page with the categories.
    """

    # Retrieving the wiki URL
    url = get_api_url()
    print(url)

    # Retrieving the pages JSON and extracting page titles
    pages_json = get_pages_json(url)
    pages = pages_json["query"]["allpages"]
    print("Pages to be scanned:", pages)

    # Tagging operations
    for page in pages:
        curr_title = page["title"]
        cats_to_add = get_categories(curr_title)
        if cats_to_add:
            print("Adding categories", cats_to_add, "to '%s'" % curr_title)
            for cat in cats_to_add:
                add_category(curr_title, "[[Category:" + cat + "]]")

    # Extracting title to continue iterating from
    if "continue" in pages_json:
        continue_from = pages_json["continue"]["apcontinue"]
        print("Continuing from:", continue_from)
    else:
        continue_from = ""

    # Continue iterating through wiki
    while continue_from:
        # Retrieving the pages JSON and extracting page titles
        pages_json = get_pages_json(url, continue_from)
        pages = pages_json["query"]["allpages"]
        print("Pages to be scanned:", pages)

        # Tagging operations
        for page in pages:
            curr_title = page["title"]
            cats_to_add = get_categories(curr_title)
            if cats_to_add:
                print("Adding categories", cats_to_add, "to '%s'" % curr_title)
                for cat in cats_to_add:
                    add_category(curr_title, "[[Category:" + cat + "]]")

        # Extracting title to continue iterating from
        if "continue" in pages_json:
            continue_from = pages_json["continue"]["apcontinue"]
            print("Continuing from:", continue_from)
        else:
            continue_from = ""

    print("No pages left to be tagged")


if __name__ == '__main__':
    main()
