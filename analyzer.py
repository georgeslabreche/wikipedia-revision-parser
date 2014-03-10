import sys
import csv
from pymongo import MongoClient

entry_title = sys.argv[1]

# connect to default local instance of mongo
client = MongoClient()

# get database and collection
db = client.revisions
collection = db.revisions

csv_filename = 'output/' + entry_title + '-revisions-per-day-count.csv'
csv_file = open(csv_filename, 'wb')
writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE)

header_ls = ['Date', 'Number of Revisions', 'Total Size of Revisions']
writer.writerow(header_ls)

print entry_title
for rev_day in collection.find({'title':entry_title}).distinct('date'):
	rev_count = collection.find({'title':entry_title, 'date':rev_day}).count()
	
	# get sum of revision sizes
	revisions_size_sum_pipe = [
		{ '$match' : { 'title' : entry_title, 'date': rev_day} },
		{ '$group' :
			{
				'_id' : '$date',
				'revisionSizePerDate' : { '$sum' : '$size' }
			}
		}
	]
	
	rev_size_sum_result = db.revisions.aggregate(pipeline=revisions_size_sum_pipe)
	day_rev_sum = rev_size_sum_result['result'][0]['revisionSizePerDate']
	
	ls = [rev_day, str(rev_count), day_rev_sum]
	
	writer.writerow(ls)
	print rev_day + " - " + str(rev_count) +  " - "  + str(day_rev_sum)
	
