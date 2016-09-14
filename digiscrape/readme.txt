sample url:

http://www.digikey.com/product-search/en/integrated-circuits-ics/embedded-microcontrollers/2556109?k=cortex+m0&k=&pkeyword=cortex+m0&pv7=17&FV=7e8007d%2Cfff40027%2Cfff800cd%2C1f140000&mnonly=0&newproducts=0&ColumnSort=0&page=1&stock=1&pbfree=1&rohs=1&quantity=0&ptm=0&fid=0&pageSize=500

example (ipython):

load digiscrape.py

url1 = 'http://www.digikey.com/product-search/en/integrated-circuits-ics/embedded-microcontrollers/2556109?k=cortex+m0&k=&pkeyword=cortex+m0&pv7=17&FV=7e8007d%2Cfff40027%2Cfff800cd%2C1f140000&mnonly=0&newproducts=0&ColumnSort=0&page=1&stock=1&pbfree=1&rohs=1&quantity=0&ptm=0&fid=0&pageSize=500'

get_best_price_per_speed(url1)

Out[14]:
[('STM32F030K6T6', '48', '1.48000'),
 ('STM32F030C6T6', '48', '1.69000'),
 ('LPC1111FHN33/102,5', '50', '1.92000'),
 ('LPC1111FHN33/103,5', '50', '1.92000'),
 ('STM32F031G4U6', '48', '1.88000')]


