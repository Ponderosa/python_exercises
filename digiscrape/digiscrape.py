# This file is used for scraping digi-key.
# It finds the best price to speed parts on a particular page.


from lxml import html
import requests


# This function returns a zipped list of the top 5 part numbers
# with price and speed
def get_best_price_per_speed(url):
    dpage = requests.get(url)
    dtree = html.fromstring(dpage.content)
    speed = get_speed(dtree)
    price = get_price(dtree)
    part = get_part_number(dtree)
    # Check for different length lists
    if len(speed) != len(price) != len(part):
        raise ValueError(
            'List lengths for price, speed, and part are not the same!')

    grouping = list(zip(part, speed, price))
    grouping_sorted = sorted(
        grouping, key=lambda group: float(group[2])/float(group[1]))
    return grouping_sorted[:5]


# This function returns a list of all speeds from page
# from top to bottom.
def get_speed(dtree):
    speed = dtree.xpath('//td[@class="CLS 143 ptable-param"]/text()')
    speed = [x.strip('\n') for x in speed]
    speed = [x.strip(' ') for x in speed]
    speed = [x.strip('\n') for x in speed]
    speed = [x.strip('MHz') for x in speed]
    return speed


# This function return a list of all the prices from page
# from top to bottom
def get_price(dtree):
    price = dtree.xpath('//td[@class="tr-unitPrice ptable-param"]/text()')
    price = [x.strip('\n') for x in price]
    price = [x.strip(' ') for x in price]
    price = [x.strip('\n') for x in price]
    return price


# This function returns a list of all the part number from page
# from top to bottom
def get_part_number(dtree):
    part_num = dtree.xpath(
        '//td[@class="tr-mfgPartNumber"]//span[@itemprop="name"]/text()')
    return part_num
