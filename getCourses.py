import urllib
import http.cookiejar
import sys
from bs4 import BeautifulSoup

headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'zh-CN,zh;q=0.9',
		'Connection':'keep-alive',
		'Referer':'http://202.115.47.141/courseSearchAction.do',
		'Upgrade-Insecure-Requests':'1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }

cookie_jar = http.cookiejar.MozillaCookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie_jar)
opener = urllib.request.build_opener(handler)

course_search_url = "http://202.115.47.141/courseSearchAction.do"

def get1stPage():
	req_1 = urllib.request.Request(course_search_url, headers = headers)
	res_1 = opener.open(req_1)

	soup_1 = BeautifulSoup(res_1.read(), 'lxml')
	token = soup_1.find('input', {'type': 'hidden'}).attrs['value']
	print('token: ', token)
	initData = (
		('org.apache.struts.taglib.html.TOKEN', token),
		('kch',''),
		('kcm',''),
		('jsm',''),
		('xsjc',''),
		('skxq',''),
		('skjc',''),
		('xaqh',''),
		('jxlh',''),
		('jash',''),
		('pageSize', 20),
		('showColumn', 'kkxsjc#开课系'),
		('showColumn', 'kch#课程号'),
		('showColumn', 'kcm#课程名'),
		('showColumn', 'kxh#课序号'),
		('showColumn', 'xf#学分'),
		('showColumn', 'kslxmc#考试类型'),
		('showColumn', 'skjs#教师'),
		('showColumn', 'xqm#校区'),
		('showColumn', 'xkxzsm#选课限制说明'),
		('pageNumber', 0), 
		('actionType', 1)
	)

	initData = urllib.parse.urlencode(initData).encode(encoding = 'GBK')
	html, nextpage_url = getHTML(course_search_url, initData)
	f = open("page1.html", 'w', encoding = 'GBK')
	f.write(html)
	f.close()

	i = 2
	while nextpage_url != None:
		nextpage_data = {'pageNumber':nextpage_url[-1], 'actionType':2}
		nextpage_data = urllib.parse.urlencode(nextpage_data).encode(encoding = 'GBK')
		html, nextpage_url = getHTML(nextpage_url, nextpage_data)
		f = open("page" + str(i) + ".html", 'w', encoding = 'GBK')
		f.write(html)
		f.close()
		i += 1
	
def getHTML(url, data):
	request = urllib.request.Request(url, data = data, headers = headers)
	soup = ''
	html = ''
	try:
		response = opener.open(request)
		print(url + "  " + str(response.code))
		html = response.read().decode('GBK', 'ignore')
		soup = BeautifulSoup(html, 'lxml')
	except urllib.error.URLError as e:
	    if hasattr(e, 'code'):
	    	print(e.code)
	    elif hasattr(e, 'reason'):
	    	print(e.reason)

	tag = soup.find('a', text = '下一页')
	if tag != None:
		nextpage_url = tag.attrs['href']
		# print("http://202.115.47.141/" + nextpage_url)

	else:
		print("This is the last page!")
		sys.exit()

	return html, "http://202.115.47.141/" + nextpage_url

if __name__ == '__main__':
	get1stPage()