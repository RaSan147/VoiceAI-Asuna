'''
Read the lates News from BBC RSS Feed.

Inspired by Kubas Google API:
https://www.sololearn.com/learn/1099/?ref=app
'''
import urllib.request as RE
from urllib.error import URLError
import xml.etree.ElementTree as ET


def check_internet(host='https://www.google.com/', timeout=3):
	if host == 'fast':
		return check_internet('http://www.muskfoundation.org/', timeout=timeout)

	elif host == 'pypi':
		return check_internet('https://pypi.org/', timeout=timeout)

	else:
		try:
			RE.urlopen(host, timeout=timeout)
			return True
		except URLError:
			return False


bbc_bit = 0
bbc_topics = {
	"Asia_url": 'http://feeds.bbci.co.uk/news/world/asia/rss.xml',
	"UK_url": 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk#',
	"Afri_url": 'http://feeds.bbci.co.uk/news/world/africa/rss.xml',
	"EU_url": 'http://feeds.bbci.co.uk/news/world/europe/rss.xml',
	"LatA_url": 'http://feeds.bbci.co.uk/news/world/latin_america/rss.xml',
	"MidE_url": 'http://feeds.bbci.co.uk/news/world/middle_east/rss.xml',
	"US_Ca_url": 'http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',
	"Eng_url": 'http://feeds.bbci.co.uk/news/england/rss.xml',
	"NIre_url": 'http://feeds.bbci.co.uk/news/northern_ireland/rss.xml',
	"Scot_url": 'http://feeds.bbci.co.uk/news/scotland/rss.xml',
	"Wales_url": 'http://feeds.bbci.co.uk/news/wales/rss.xml',
	"top_url": 'http://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml?edition=uk',
	"world_url": 'http://feeds.bbci.co.uk/news/video_and_audio/world/rss.xml',
	"busi_url": 'http://feeds.bbci.co.uk/news/video_and_audio/business/rss.xml',
	"tech_url": 'http://feeds.bbci.co.uk/news/video_and_audio/technology/rss.xml',
	"science_url": 'http://feeds.bbci.co.uk/news/video_and_audio/science_and_environment/rss.xml',
	"polit_url": 'http://feeds.bbci.co.uk/news/video_and_audio/politics/rss.xml',
	"entertain_url": 'http://feeds.bbci.co.uk/news/video_and_audio/entertainment_and_arts/rss.xml',
	"health_url": 'http://feeds.bbci.co.uk/news/video_and_audio/health/rss.xml'
}


class BBC_News:

	def __init__(self):
		self.last_news = None

	def news_report(self,x):
		link = bbc_topics[x]
		data = RE.urlopen(link).read()
		# print(data)
		tree = ET.fromstring(data)
		x = data.find(b'lastBuildDate') + 14
		lastupdate = data[x:x + 29].decode('utf-8')

		report = ''
		news_list = []
		report += '\nThis are the latest News at the BBC:\n(updated on:%s)\n' % lastupdate
		news_list.append(report)

		for i in tree.iter('item'):
			title = i.find('title')
			description = i.find('description')
			try:
				ok =  (title.text and description.text)
			except Exception:
				continue
			if not ok:
				continue
			news = '/hui/• {}: /=/\n-- {}\n'.format(title.text, description.text)
			news += "/s1/" + '\n'
			report += news
			news_list.append(news)

		self.last_news = news_list
		return news_list


	# print(__name__)
	def task(self, Topic):
		if __name__ == '__main__':
			if check_internet(bbc_topics[Topic]):
				from PRINT_TEXT3 import xprint
				xprint(*self.news_report(Topic), wait_time= 0.03)
				# print(*self.news_report(Topic))
			else:
				print('Could not access the server')
		else:
			return self.news_report(Topic)

bbc_news = BBC_News()


if __name__ == '__main__':
	bbc_news.task('Asia_url')
