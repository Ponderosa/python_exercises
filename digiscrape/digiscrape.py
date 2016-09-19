"""
This package is used for scraping digi-key.
It finds the best price to speed parts on a particular page.
"""

from lxml import html
import requests


def get_best_price_per_speed(url, max_parts=5):
    """Return a list of tubles of the part numbers with the best price and speed.

    Args:
        url (str): digikehy url to scrape
        max_parts (int, defualt=5): return at most this many results.
    """
    dpage = requests.get(url)
    dtree = html.fromstring(dpage.content)
    speed = get_speed(dtree)
    price = get_price(dtree)
    part = get_part_number(dtree)
    # Check for different length lists
    if len(speed) != len(price) != len(part):
        raise ValueError(
            'List lengths for price, speed, and part are not the same!')

    grouping = zip(part, speed, price)
    grouping_sorted = sorted(
        grouping, key=lambda group: float(group[2])/float(group[1]))
    return grouping_sorted[:max_parts]


def get_speed(dtree):
    """Return a list of all speeds from page from top to bottom.

    Args:
        dtree: ??? what is the type ???
    """
    speed = dtree.xpath('//td[@class="CLS 143 ptable-param"]/text()')
    speed = [x.strip('\n \nMHz') for x in speed]
    return speed


def get_price(dtree):
    """Return a list of all prices from page from top to bottom.

    Args:
        dtree: ??? what is the type ???
    """
    price = dtree.xpath('//td[@class="tr-unitPrice ptable-param"]/text()')
    price = [x.strip('\n \n') for x in price]
    return price


# This function returns a list of all the part number from page
# from top to bottom
def get_part_number(dtree):
    """ Return a list of all part numbers from page from top to bottom.

    Args:
      dtree: ??? what is the type ???

    """
    part_num = dtree.xpath(
        '//td[@class="tr-mfgPartNumber"]//span[@itemprop="name"]/text()')
    return part_num
