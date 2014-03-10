import sys
import urllib
from datetime import datetime
from xml.dom import minidom
from pymongo import MongoClient

entry_title = sys.argv[1]
wp_api_rev_url = 'http://en.wikipedia.org/w/api.php?action=query&titles=' + entry_title + '&prop=revisions&rvlimit=500&rvdir=newer&rvprop=ids|flags|user|userid|size|timestamp|comment&format=xml'


more_revisions_left = True
rvcontinue = ''

# connect to default local instance of mongo
client = MongoClient()

# get database and collection
db = client.revisions
collection = db.revisions

while more_revisions_left:
	if not rvcontinue:
		revisions_xml_url = wp_api_rev_url
	else:
		revisions_xml_url = wp_api_rev_url + '&rvstartid=' + rvcontinue
	
	print revisions_xml_url

	xmldoc = minidom.parse(urllib.urlopen(revisions_xml_url))
	revisions = xmldoc.getElementsByTagName('rev') 

	for rev in revisions:
		revid = int(rev.attributes['revid'].value)
		parentid = int(rev.attributes['parentid'].value)
		
		if rev.hasAttribute('user'):
			user = rev.attributes['user'].value
			userid = int(rev.attributes['userid'].value)
		else:
			user = -1
			userid = -1
		
		revision_size = int(rev.attributes['size'].value)

		timestamp_str = rev.attributes['timestamp'].value
		timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
		date_str = timestamp_str[:10]
		
		revision_post = {"title":entry_title, "revid":revid, "parentid":parentid, "user":user, "userid":userid, "size":revision_size, "date":date_str, "timestamp":timestamp}
		
		post_id = collection.insert(revision_post)
		
		print revision_post

	# Check if there are more revisions left
	query_continue = xmldoc.getElementsByTagName('query-continue')
	if query_continue:
		rvcontinue = query_continue.item(0).getElementsByTagName('revisions').item(0).attributes['rvcontinue'].value
	else:
		more_revisions_left = False
    
