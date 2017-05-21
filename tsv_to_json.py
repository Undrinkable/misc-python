import sys
import json

def main():
	if len(sys.argv) < 2:
		print("Missing arguments.\nUsage: python tsv_to_json.py [infile]\nTSV file must have a header row containing the column names. The first column will be used as key")
		exit()

	with open(sys.argv[1]) as infile:
		content = infile.readlines()

	header_line = content[0]
	item_names = header_line.split('\t')

	data_json = {}
	for i in xrange(1, len(content)):
		content[i] =  content[i].replace("\n","")

		properties = content[i].split('\t')

		item_json = {}
		for i in xrange(1, len(properties)):
			item_json[item_names[i].rstrip("\r\n")] = properties[i].rstrip("\r\n")
		data_json[properties[0]] = item_json

	print json.dumps(data_json)


if __name__ == '__main__':
	main()