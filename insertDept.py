import pymysql
import urllib.request
from getCourses import headers, course_search_url
from bs4 import BeautifulSoup

db = pymysql.connect("localhost", "root", "hanjin", "scucoursereview", charset = 'gbk')
cursor = db.cursor()

def insert2DB():
	req = urllib.request.Request(course_search_url, headers = headers)
	res = urllib.request.urlopen(req)
	soup = BeautifulSoup(res.read(), 'lxml')

	depts = soup.find('select', {'name':'xsjc'}).find_all('option')
	for e in depts[1:]:
		dept = e.attrs['value']
		sql = "insert into main_department(content) values(%s);"
		try:
			cursor.execute(sql, (dept))
			db.commit()
		except Exception as e:
			db.rollback()
		print(dept + " insert successfully!")

if __name__ == '__main__':
	insert2DB()