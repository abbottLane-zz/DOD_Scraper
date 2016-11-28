import re
import urlparse

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


county="King%20county"
year_span = "2011-2014"
count=75
link = "https://familysearch.org/search/collection/results?count="+str(count)+"&query=%2Bdeath_place%3A%22"+county+"%22~%20%2Bdeath_year%3A"+year_span+"~&collection_id=1202535"
#link="https://familysearch.org/ark:/61903/1:1:JTL6-NY9"
print "Executing Query: " + link

class FamilySearchDODScraper(object):
    def __init__(self):
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
        # )
        #self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])
        self.driver = webdriver.Firefox(executable_path="/home/wlane/Applications/geckodriver")
        self.driver.set_window_size(1120, 550)


    def scrape_job_links(self):
        self.driver.get(link)
        self.hey_driver_wait_for_load()
        jobs = []
        pageno = 2

        self.driver.save_screenshot('screen.png')
        while True:
            s = BeautifulSoup(self.driver.page_source, "html.parser")
            print s
            r = re.compile(r'https://familysearch\.org/ark:/\d+/.+')

            row_results = s.find_all('a', href=r)
            for a in row_results:
                tr = a.findParent('tr')
                td = tr.findAll('td')

                person = {}
                person['name'] = a.text
                person['url'] = urlparse.urljoin(link, a['href'])
                person['data'] = td[2].text
                jobs.append(person)
            # for debug: early break
            break

            next_page_elem = self.driver.find_element_by_link_text('Next')#find_element_by_id('paging')
            next_page_link = s.find('a', text='%d' % pageno)

            if next_page_link:
                next_page_elem.click()
                pageno += 1
                sleep(5)
            else:
                break

        return jobs

    def hey_driver_wait_for_load(self):
        try:
            WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.LINK_TEXT,"Next"))) #DataTables_Table_0
            #sleep(5)
        except TimeoutException:
            print "A timeout occured!!"

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
    scraper = FamilySearchDODScraper()
    scraper.scrape()