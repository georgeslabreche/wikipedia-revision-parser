from pymongo import MongoClient
import csv

# connect to default local instance of mongo
client = MongoClient()

# get database and collection
db = client.revisions
collection = db.kosovo

for rev_day in collection.distinct("date"):
	rev_count = collection.find({"date":rev_day}).count()
	print rev_day + ": " + str(rev_count)
	
	'''
	csv_file = open('result.csv', 'wb')
	writer = csv.writer(csv_file, delimiter=',')
	writer.writerow(rev_day)
	'''