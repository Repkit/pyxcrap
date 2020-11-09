import scrapy
import requests
from time import sleep


start_urls = []
url = 'https://www.studystore.nl' 

organisations = requests.get(url + '/api/ListApi/GetOrganizationsAsync/')

for org in organisations.json():
	orgId = org['Id']
	orgName = org['Url']
	orgdeps = requests.get(url + '/api/ListApi/GetDepartmentsByOrganizationIdAsync/?organizationId=' + orgId)
	for dep in orgdeps.json():
		depId = dep['Id']
		periods = requests.get(url + '/api/ListApi/GetPeriods/?parentId=' + depId)
		for period in periods.json():
			periodId = period['Id']
			periodName = period['Url']
			groups = requests.get(url + '/api/ListApi/GetGroups/?periodId=' + periodId)
			for group in groups.json():
				groupId = group['Id']
				bookLists = requests.get(url + '/api/ListApi/GetBooklists/?parentId=' + groupId + '&periodId=' + periodId)
				for blist in bookLists.json():
					schoolNo = blist['SchoolListNumber']
					bookList = blist['Url']
					scrapurl = url + '/boekenlijst/' + orgName + '/' + periodName + '/' + schoolNo + '/' + bookList
					filename = '/scripts/to-scrap-url.txt'
					f = open(filename, "a")
					f.write(scrapurl)
					f.write('\n')
					f.close
					start_urls.append(scrapurl)
					# books = requests.get(url + '/boekenlijst/' + orgName + '/' + periodName + '/' + schoolNo + '/' + bookList)
					# print(books.text)
					sleep(0.05)
					# break
				sleep(0.05)
				# break
			sleep(0.05)	
			# break
		sleep(0.05)	
		# break
	sleep(0.05)	
	# break

class StorenlSpider(scrapy.Spider):
    name = 'storenlspirder'

    print(start_urls)

    # def parse(self, requestssponse):
    #     for title in response.css('.post-header>h2'):
    #         yield {'title': title.css('a ::text').get()}

    #     for next_page in response.css('a.next-posts-link'):
    #         yield response.follow(next_page, self.parse)
