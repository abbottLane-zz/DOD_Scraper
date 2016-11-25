import re
import urlparse

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

from selenium.webdriver import DesiredCapabilities

county="King%20county"
year_span = "2011-2014"
link = "https://familysearch.org/search/collection/results?count=20&query=%2Bdeath_place%3A%22"+county+"%22~%20%2Bdeath_year%3A"+year_span+"~&collection_id=1202535"
# link= "https://www.google.com/search?client=ubuntu&channel=fs&q=test&ie=utf-8&oe=utf-8"
print "Executing Query: " + link
print "pause"

class TaleoJobScraper(object):
    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
        )
        #self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'], executable_path=r"C:\Users\William\Downloads\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe")
        self.driver.set_window_size(1120, 550)

    def scrape_job_links(self):
        self.driver.get(link)

        jobs = []
        pageno = 2

        print "Wating 10 seconds....because otherwise this wont work..."
        for i in range(10):
            sleep(1)
            print i+1


        while True:
            s = BeautifulSoup(self.driver.page_source, "html.parser")
            self.driver.save_screenshot('screen.png')
            print s
            r = re.compile(r'https://familysearch\.org/ark:/\d+/.+')

            row_results = s.find_all('a', href=r)
            for a in row_results:
                tr = a.findParent('tr')
                td = tr.findAll('td')

                job = {}
                job['title'] = a.text
                job['url'] = urlparse.urljoin(link, a['href'])
                job['location'] = td[1].text
                jobs.append(job)

            next_page_elem = self.driver.find_element_by_id('next')
            next_page_link = s.find('a', text='%d' % pageno)

            if next_page_link:
                next_page_elem.click()
                pageno += 1
                sleep(.75)
            else:
                break

        return jobs

    def scrape_job_descriptions(self, jobs):
        for job in jobs:
            self.driver.get(job['url'])

            s = BeautifulSoup(self.driver.page_source)
            x = {'class': 'mastercontentpanel3'}
            d = s.find('div', attrs=x)

            if not d:
                continue

            job['desc'] = ' '.join(d.findAll(text=True))
            sleep(.75)

    def scrape(self):
        jobs = self.scrape_job_links()
        for job in jobs:
            print job

        self.driver.quit()

if __name__ == '__main__':
    scraper = TaleoJobScraper()
    scraper.scrape()