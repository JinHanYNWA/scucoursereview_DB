# scucoursereview_DB
## The databases of website scucoursereview.com


* ### getCourses.py:<br>
    Firstly I create a spider to get all the courses from "http://202.115.47.141/courseSearchAction.do", where you can search all the courses in this semester in SCU. I store them in ".html" format.


* ### insertDept.py:<br>
    Secondly I get all the departments on the same website, and insert all of them into table "main_department".


* ### insertCourses.py:<br>
    Finally I create another spider to get the concrete information of every course from those ".html" files that I got in step 1. And then insert the information into table "main_course".
