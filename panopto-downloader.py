from lxml import etree
import urllib2
import string

def download_file(url, file_name):
	file_name = ''.join(c if c not in ['/'] else '.' for c in file_name)
	print file_name

	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()

# url = "http://panopto.imperial.ac.uk/Panopto/Podcast/Podcast.ashx?courseid=506badc8-555e-47dc-a216-fe5ec8a43ded&type=mp4"
url = raw_input('Enter Panopto Podcast URL:')

html = urllib2.urlopen(url)

r = etree.parse(html)

lectures = r.xpath('//item/itunes:summary', 
					namespaces = {'itunes' : 'http://www.itunes.com/dtds/podcast-1.0.dtd'})


for string in ['({0}) {1}'.format(n+1,l.text) for (n,l) in enumerate(lectures)]:
	print string
print '({0}) Download all'.format(len(lectures)+1)

option = int(raw_input('Enter option:'))

if (option == len(lectures)+1):
	download = lectures
elif option in range(1,len(lectures)+1):
	print 'valid'
	download = [lectures[option-1]]
else:
	print 'Invalid option.'
	raise SystemError


for lecture in download:
	download_file(lecture.xpath('../guid')[0].text,lecture.text+'.mp4')

