from bs4 import BeautifulSoup
import pymysql
import sys

db = pymysql.connect("localhost", "root", "hanjin", "scucoursereview", charset = 'gbk')
cursor = db.cursor()

for i in range(1, 375):
	soup = BeautifulSoup(open("page" + str(i)+ ".html"), 'lxml')
	courses = soup.find_all('tr', class_ = "odd")
	
	for j in range(len(courses)):
		items = courses[j].find_all('td')
		insert_content = []
		for k in range(len(items)):# 9 items
			# print(str(item[k].getText()).replace(u'\xa0', u' ').strip(), end = '\t')
			item = str(items[k].getText()).replace(u'\xa0', u'').strip().replace('\n', '')
			if k == 0:
				sql_find = "select id from main_department where content = %s"
				cursor.execute(sql_find, (item))
				result = cursor.fetchone()
				insert_content.append(result[0])
			elif k == 1:
				insert_content.append(item)
			elif k == 2:
				insert_content.append(item)
			elif k == 3:
				insert_content.append(item)
			elif k == 4:
				insert_content.append(float(item))
			elif k == 5:
				insert_content.append(item)
			elif k == 6:
				insert_content.append(item)
			elif k == 7:
				sql_find = "select id from main_campus where content = %s"
				cursor.execute(sql_find, (item))
				result = cursor.fetchone()
				if result == None:
					insert_content.append(4)
					continue
				insert_content.append(result[0])
			else:
				insert_content.append(item)
		sql_insert = '''insert into main_course(department_id, course_id, name, course_order, credit, assessment_method, professors, campus_id, limitation, semester_id) 
						values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
		insert_content.pop()
		insert_content.append(1)
		try:
			cursor.execute(sql_insert, (insert_content))
			db.commit()
		except Exception as e:
			db.rollback()
			print(e)
	print("page" + str(i) + " is OK!")
