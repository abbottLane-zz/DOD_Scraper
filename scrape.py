import FSDODQueryProcessor
from FSDODScraper import FamilySearchDODScraper
from DBAccessController import DBAccess

scraper = FamilySearchDODScraper()
people = scraper.scrape()
dbaccess = DBAccess("dev") # arg is the name of the db entry in dbaccessconfig.ini
for person in people:
    add_person_query = FSDODQueryProcessor.build_add_person_query(person, dbaccess.db_env)
    dbaccess.execute_INSERT_INTO_query(add_person_query)
print "Done."
