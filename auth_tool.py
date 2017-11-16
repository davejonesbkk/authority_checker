from mozscape import Mozscape
import csv, time, math, argparse

def parse_sites(sites_file):

	#get the list of websites for testing
	with open(sites_file) as sl:
		sites = [x.strip() for x in sl.readlines()]

	#create an empty list to store the websites
	sites_list = []

	for s in sites:
		sites_list.append(s)

	#get MOZ API credentials
	with open('keys.txt') as fp:
		credentials = [x.strip() for x in fp.readlines()]

	moz_id = credentials[0]
	moz_key = credentials[1]

	#access the MOZ client using credentials
	client = Mozscape(moz_id, moz_key)

	#creating new list for storing websites MOZ DA data
	sites_data = []

	for i in sites_list:

			print 'Getting DA data for ', i
			i = client.urlMetrics([i], Mozscape.UMCols.domainAuthority)
			sites_data.append(math.ceil(i[0]['pda']))
			print 'Complete. Going to next domain in list'
			print '...'
			time.sleep(5)


	#create a dictionary for storing the websites and their MOZ metrics
	sites_metrics = dict(zip(sites_list, sites_data))

	print sites_metrics

	print 'Saving to file'

	to_file(sites_metrics)


def to_file(sites_metrics):

	#save websites and data to csv file		
	with open('sites_data.csv', 'wb') as sd:
		writer = csv.writer(sd) 
		writer.writerow(["Domain", "Domain Authority"])
		for row in sites_metrics.iteritems():
		#writer.writeheader()
			writer.writerow(row)

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('sites_file', help='Enter the file name where your sites are stored')
	args = parser.parse_args()

	sites_file = args.sites_file

	parse_sites(sites_file)


if __name__ == '__main__':
	main()




