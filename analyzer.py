import sys
import csv
from pymongo import MongoClient

entry_title = sys.argv[1]

# connect to default local instance of mongo
client = MongoClient()

# get database and collection
db = client.revisions
collection = db.revisions

csv_filename = entry_title + '-revisions-per-day-count.csv'
csv_file = open(csv_filename, 'wb')
writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)

print entry_title
for rev_day in collection.find({'title':entry_title}).distinct('date'):
	rev_count = collection.find({'title':entry_title, 'date':rev_day}).count()
	
	ls = [rev_day, str(rev_count)]
	
	writer.writerow(ls)
	print rev_day + ": " + str(rev_count)
	