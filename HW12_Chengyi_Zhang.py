import flask
import jinja2
import sqlite3
import os.path
from typing import Dict, List


app = flask.Flask(__name__)


@app.route('/Hello')
def hello() -> str:
    return "Hello World!"


@app.route('/Table')
def students_summary() -> str:
    query = "select s.Name , s.CWID, g.Course, g.Grade, i.Name from students s join grades g on s.CWID = " \
           "g.StudentCWID join instructors i on g.InstructorCWID = i.CWID order by s.Name "
    db: sqlite3.Connection = sqlite3.connect('810_Database.db')
    students: List[Dict[str, str]] = [{'Name': name, 'CWID': cwid, 'Course': course, 'Grade': grade, 'Instructor': instructor}
                                      for name, cwid, course, grade, instructor in db.execute(query)
                                      ]
    db.close()
    return flask.render_template('base.html',
                                 title='Stevens Repository',
                                 table_title='Student, Course, Grade, and Instructor',
                                 students_summary=students)


# Run the Flask app
app.run(debug=True)

