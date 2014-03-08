import urllib
from xml.dom import minidom
from pymongo import MongoClient

WP_KOSOVO_REVISIONS_API_URL = 'http://en.wikipedia.org/w/api.php?action=query&titles=Kosovo&prop=revisions&rvlimit=500&format=xml'

more_revisions_left = True
rvcontinue = ''

# connect to default local instance of mongo
client = MongoClient()

# get database and collection
revisions_db = client.revisions
kosovo_collection = revisions_db.kosovo

while more_revisions_left:
	if not rvcontinue:
		revisions_xml_url = WP_KOSOVO_REVISIONS_API_URL
	else:
		revisions_xml_url = WP_KOSOVO_REVISIONS_API_URL + '&rvstartid=' + rvcontinue
	
	print revisions_xml_url

	xmldoc = minidom.parse(urllib.urlopen(revisions_xml_url))
	revisions = xmldoc.getElementsByTagName('rev') 

	for rev in revisions:
		timestamp = rev.attributes['timestamp'].value
		revid = rev.attributes['revid'].value
		date_str = timestamp[:10]
		
		revision_post = {"revid":revid, "date":date_str, "timestamp":timestamp}
		
		post_id = kosovo_collection.insert(revision_post)
		
		print revision_post

	# Check if there are more revisions left
	query_continue = xmldoc.getElementsByTagName('query-continue')
	if query_continue:
		rvcontinue = query_continue.item(0).getElementsByTagName('revisions').item(0).attributes['rvcontinue'].value
	else:
		more_revisions_left = False
    
