import sys
import csv
from pymongo import MongoClient

entry_title = sys.argv[1]

# connect to default local instance of mongo
client = MongoClient()

# get database and collection
db = client.revisions
collection = db.revisions

csv_filename = entry_title + '-number-of-revisions-per-user.csv'
csv_file = open(csv_filename, 'wb')
writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

header_ls = ['Username', 'Number of Revisions', "Total Size of Revisions"]
writer.writerow(header_ls)

print entry_title
for rev_user in collection.find({'title':entry_title}).distinct('user'):
	rev_count = collection.find({'title':entry_title, 'user':rev_user}).count()
	
	# get sum of revision sizes
	revisions_size_sum_pipe = [
		{ '$match' : { 'title' : entry_title, 'user': rev_user} },
		{ '$group' :
			{
				'_id' : '$user',
				'revisionSizePerUser' : { '$sum' : '$size' }
			}
		}
	]
	
	rev_size_sum_result = db.revisions.aggregate(pipeline=revisions_size_sum_pipe)
	user_rev_size_sum = rev_size_sum_result['result'][0]['revisionSizePerUser']
	
	ls = [unicode(rev_user).encode("utf-8"), str(rev_count), user_rev_size_sum]
	
	writer.writerow(ls)
	print rev_user + " - " + str(rev_count) +  " - "  + str(user_rev_size_sum)
	
	
