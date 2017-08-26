import requests 
import sys
import argparse, csv, time, math 
from urlparse import urlparse
from bs4 import BeautifulSoup
from mozscape import Mozscape 
import pandas as pd


reload(sys)
sys.setdefaultencoding('utf-8')

with open('keys.txt', 'r') as fp:
	credentials = [x.strip() for x in fp.readlines()]

moz_id = credentials[0]
moz_key = credentials[1]

client = Mozscape(moz_id, moz_key)


def page_parser(url):

	links_list = []
	r = requests.get(url)
	html = r.text
	soup  = BeautifulSoup(html, "html.parser")
	print soup.title 
	for link in soup.find_all('a'):
		links_list.append(link.get('href'))
		
	domain_parse(links_list)
	
def domain_parse(links_list):

	domains = []
	
	for l in links_list:
		l = urlparse(l)
		domains.append(l.netloc)
		
	domain_check(domains, links_list)	
		
def domain_check(domains, links_list):

	sites_data = []

	for d in domains:
		print 'Getting data for ', d 
		d = client.urlMetrics([d], Mozscape.UMCols.domainAuthority)
		sites_data.append(math.ceil(d[0]['pda']))
		print 'Complete. Going to next domain in the list...'
		print '....'
		time.sleep(5)
		
	
	pandas_data = pd.DataFrame(
		{'links_list': links_list,
		'domains': domains,
		'DA': sites_data})
		
	to_file(sites_metrics)
		
	
def to_file(data):

	with open('sites_metrics.csv', 'wb') as fp:
		writer = csv.writer(fp)
		writer.writerow(['Domain', 'Guest post page', 'Domain Authority'])
		for row in site_metrics.iteritems():
			writer.writerow(row)
							
		

def site_data():
	parser = argparse.ArgumentParser()
	parser.add_argument('target_url', help='Enter the full url of the page you wish to parse')
	args = parser.parse_args()
	
	url = args.target_url
	
	page_parser(url)
	

if __name__ == '__main__':
	site_data()
	
	

	
	
	

	
	
	
	

	



