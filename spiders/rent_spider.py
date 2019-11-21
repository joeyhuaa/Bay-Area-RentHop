import scrapy
from ..items import Item

# always include scrapy.Spider as parameter!
class RentHopSpider(scrapy.Spider):

  # don't change these variable names!
  name = 'rents'
  page_num = 1
  start_urls = [
    'https://www.renthop.com/search/san-francisco-bay-area-ca?min_price=0&max_price=50000&q=&neighborhoods_str=&sort=hopscore&page=1&search=0'
  ]

  def parse(self, response):

    items = Item()

    listings = response.css('div.search-listing')

    for listing in listings:

      # these are easy to retrieve
      district = listing.css('.font-size-9.overflow-ellipsis::text').extract()[0].strip()
      county = district.split(',').pop().strip()
      rent = int(listing.css('td.font-size-11.b::text').extract()[0].strip().split('$')[1].replace(',', ''))
      bed = listing.css('.b span::text').extract()[0].strip().split(' ')[0]
      bath = float(listing.css('.b span::text').extract()[1].split(' ')[0])

      # these require more work to retrieve
      area = None
      special1 = None
      special2 = None

      area_specials = listing.css('div.font-size-9::text').extract().pop().strip().split(' · ')

      #if square footage is there
      if any(char.isdigit() for char in area_specials[0]):
        area = area_specials[0].split(' ')[0].replace(',', '')

        try:
          special1 = area_specials[1]
          special2 = area_specials[2]
        except IndexError:
          pass

      # if square footage isn't there
      else:
        try:
          special1 = area_specials[0]
          special2 = area_specials[1]
        except IndexError:
          pass

      items['district'] = district
      items['county'] = county
      items['rent'] = rent
      items['bed'] = bed
      items['bath'] = bath
      items['area'] = area
      items['special1'] = special1
      items['special2'] = special2

      yield items

      # keep getting next pages
      next_url = 'https://www.renthop.com/search/san-francisco-bay-area-ca?min_price=0&max_price=50000&q=&neighborhoods_str=&sort=hopscore&page=' + str(RentHopSpider.page_num) + '&search=0'

      if RentHopSpider.page_num <= 147:
        RentHopSpider.page_num += 1
        yield response.follow(next_url, callback=self.parse)