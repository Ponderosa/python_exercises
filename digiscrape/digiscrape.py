"""
This package is used for scraping digi-key.
It finds the best price to speed parts on a particular page.
"""

from lxml import html
import requests


def get_best_price_per_speed(url, max_parts=5):
    """Return a list of tuples of the part numbers with the best price and speed.

    Args:
        url (str): digikey url to scrape
        max_parts (int, default=5): return at most this many results.
    """
    # Create web structure data
    page = requests.get(url)
    html_tree = html.fromstring(page.content)

    # Create lists for speed, price, and part numbers
    speed = list(get_speeds(html_tree))
    price = list(get_prices(html_tree))
    part = list(get_part_numbers(html_tree))

    # Check for different length lists
    if len(speed) != len(price) != len(part):
        raise ValueError(
            'List lengths for price, speed, and part are not the same!')

    # Group and sort
    grouping = zip(part, speed, price)
    grouping_sorted = sorted(
        grouping, key=lambda group: float(group[2])/float(group[1]))
    return grouping_sorted[:max_parts]


def get_items(tree, xpath, chars_to_strip=None, parse_as=str):
    """Return generator over the cleaned items provided by xpath

    Args:
        tree (ElementTree): html tree
        xpath: path to search for on html tree
        chars_to_strip (str): remove these characters before parsing the str.
            Defaults to stripping whitespace.
        parse_as (str -> ?): optional function used to parse the item as a
            different data type.  defaults to leaving the item as a string.
    """
    return (parse_as(x.strip(chars_to_strip)) for x in tree.xpath(xpath))


def get_speeds(tree):
    """Return a generator of all speeds from page from top to bottom.

    Args:
        tree (ElementTree): html tree
    """
    return get_items(
        tree,
        '//td[@class="CLS 143 ptable-param"]/text()',
        chars_to_strip='\n MHz',
        parse_as=float)


def get_prices(tree):
    """Return a generator of all prices from page from top to bottom.

    Args:
        tree (ElementTree): html tree
    """
    return get_items(
        tree,
        '//td[@class="tr-unitPrice ptable-param"]/text()',
        chars_to_strip=' \n',
        parse_as=float)


def get_part_numbers(tree):
    """ Return a generator of all part numbers from page from top to bottom.

    Args:
      tree (ElementTree): html tree

    """
    return get_items(
        tree,
        '//td[@class="tr-mfgPartNumber"]//span[@itemprop="name"]/text()')
