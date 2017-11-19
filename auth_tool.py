
#Get each domains DA score, total linking domains, ip address
#Use Pandas to put into a dataframe and then save to csv


from mozscape import Mozscape
import csv, time, math, argparse, socket

import pandas as pd


def parse_sites(sites_file):

	#get the list of websites for testing
	with open(sites_file) as sl:
		sites = [x.strip().lstrip('http://').rstrip('/') for x in sl.readlines()]
		
	print(sites)	
	

	#get MOZ API credentials
	with open('keys.txt') as fp:
		credentials = [x.strip() for x in fp.readlines()]

	moz_id = credentials[0]
	moz_key = credentials[1]

	#access the MOZ client using credentials
	client = Mozscape(moz_id, moz_key)

	#creating new list for storing websites MOZ DA data
	sites_da = []
	sites_backlinks = []
	sites_ips = []

	for i in sites:

			print 'Getting DA data for ', i
			i = client.urlMetrics([i], Mozscape.UMCols.domainAuthority)
			sites_da.append(math.ceil(i[0]['pda']))
			print 'Complete. Going to next domain in list'
			print '...'
			time.sleep(5)
			
	for k in sites:		
			
		print 'Getting total backlinks for ', k 
		k = client.urlMetrics([k], Mozscape.UMCols.links)
		sites_backlinks.append(k[0]['uid'])
		print 'Complete. Going to next domain in list'
		print '...'
		time.sleep(5)		
		
	for s in sites:
	
		try:
	
			print 'Getting the ip address of ', s 
			s = socket.gethostbyname(s)
			sites_ips.append(s)
			
		except:
			print 'Could not get ip address for ', s
			sites_ips.append('Error getting ip')
			continue
			
	
			

	#create a dictionary for storing the websites, their DA score and number of backlinks
	sites_metrics = dict(zip(sites, zip(sites_da, sites_backlinks, sites_ips)))

	print sites_metrics

	
	
	df = pd.DataFrame.from_dict(data=sites_metrics, orient='index')
	df.columns = ['Domain Authority', 'Backlinks', 'IP']
	
	print(df)

	to_file(df)


def to_file(df):

	print 'Saving to file'

	df.to_csv('sites_data.csv')
	

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('sites_file', help='Enter the file name where your sites are stored')
	args = parser.parse_args()

	sites_file = args.sites_file

	parse_sites(sites_file)


if __name__ == '__main__':
	main()




