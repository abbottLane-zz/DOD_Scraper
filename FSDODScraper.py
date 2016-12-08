import json
import re
import urlparse

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


county="seattle"#"King%20county"
year_span = "2002-2002"
count=75
obit_collection="2333694"
SS_master_death_collection = "1202535"
link = "https://familysearch.org/search/collection/results?count="+str(count)+"&query=%2Bdeath_place%3A%22"+county+"%22~%20%2Bdeath_year%3A"+year_span+"~&collection_id="+obit_collection
print "Executing Query: " + link


def write_people(people):
    with open('outputs/ObitCollectionExamples.out', 'w') as outfile:
        json.dump(people, outfile, indent=4, sort_keys=True)


class FamilySearchDODScraper(object):
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="/home/wlane/Applications/geckodriver", log_path="outputs/geckodriver.log")
        self.driver.set_window_size(1120, 550)

    def scrape_job_links(self):
        self.driver.get(link)
        self.hey_driver_wait_for_load()
        jobs = []
        pageno = 2

        self.driver.save_screenshot('outputs/screen.png')
        while True:
            s = BeautifulSoup(self.driver.page_source, "html.parser")
            r = re.compile(r'https://familysearch\.org/ark:/\d+/.+')

            row_results = s.find_all('a', href=r)
            for a in row_results:
                tr = a.findParent('tr')
                td = tr.findAll('td')

                person = {}
                person['name'] = a.text
                person['url'] = urlparse.urljoin(link, a['href'])
                person['data'] = td[2].text
                person['relationships'] = td[3].text
                if person['name'] != "":
                    jobs.append(person)

            # #debug: early break for testing
            #break

            next_page_elem = self.driver.find_element_by_link_text('Next')
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
        people = self.scrape_job_links()
        write_people(people)
        self.driver.quit()
        return people


if __name__ == '__main__':
    scraper = FamilySearchDODScraper()
    people = scraper.scrape()