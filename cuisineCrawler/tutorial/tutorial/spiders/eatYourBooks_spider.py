from scrapy.spider import BaseSpider

class eatYourBooksSpider(BaseSpider):
	name="eatYourBooks"
	allowed_domains=["eatyourbooks.com"]
	start_urls=[
		"http://www.eatyourbooks.com/recipes/indian",
		"http://www.eatyourbooks.com/library/16616/at-home-with-madhur-jaffrey"
	]

	def parse(self,response):
		hx=HtmlXPathSelector(response)
		recipes=hx.select('//div/h2')
		for recipe in recipes:
			link=recipe.select('a/@href').extract()
			title=recipe.select('a/text()').extract()
			desc=recipe.select('text()').extract()
			print link, title, desc
		entityDetails=hx.select('//ul/li')
		for entityDetail in entityDetails:
			entityType=entityDetail.select('span/@entityType').extract()
			entityId=entityDetail.select('span/@entityId').extract()
			
		filename=response.url.split("/")[-2]
		open(filename,'wb').write(response.body)
