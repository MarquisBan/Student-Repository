from prettytable import PrettyTable
from typing import List, Tuple
from collections import defaultdict


class Students:
    def __init__(self, cwid: str, name: str, dpt: str):
        self._cwid = cwid
        self._name = name
        self._dept = dpt

    def set_cg(self, courseandgrades: dict):
        self._cg = courseandgrades


class Instructors:
    def __init__(self, cwid: str, name: str, dpt: str):
        self._cwid = cwid
        self._name = name
        self._dept = dpt

    def set_co(self, courseandstu: dict):
        self._course = courseandstu


class University:
    def __init__(self, name: str):
        self._name = name
        self._students: List[Students] = []
        self._instructors: List[Instructors] = []

    def set_stu(self, stus: List[Students]):
        self._students = stus

    def set_ins(self, inss: List[Instructors]):
        self._instructors = inss

    def ptprint(self) -> None:
        pts = PrettyTable(['CWID', 'Name', 'Completed Courses'])
        pti = PrettyTable(['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for one in self._students:
            pts.add_row([one._cwid, one._name, sorted(list(one._cg.keys()))])
        for one in self._instructors:
            for course in one._course:
                pti.add_row([one._cwid, one._name, one._dept, course, one._course[course]])

        print("Student Summary")
        print(pts)
        print("Instructor Summary")
        print(pti)


unvst: str = input("Please input the university name, which is also the name of directory: ")
# Build the instance of University
uni = University(unvst)


# file_reader from HW08
def file_reader(path, fields, sep=',', header=False):
    """ Read a table-like file with columns and rows """
    try:
        fs = open(path, 'r')
        lines = fs.readlines()
        fs.close()
    except FileNotFoundError:
        print("ERROR!!!")
        print("Cannot find the file with the path given")
        raise SystemExit

    if '\\' in path:
        temp = path.rindex('\\')
        filename = path[temp + 1:]
    else:
        filename = path

    for i in range(len(lines)):
        line = lines[i]
        ss = line.strip().split(sep)
        temp = len(ss)
        if temp != fields:
            raise ValueError(f"'{filename}' has {temp} fields on line {i} but expected {fields}")
        if not header or i > 0:
            yield ss


# read the information of this university
stu = file_reader(''.join([unvst, '\\students.txt']), 3, '	')
ins = file_reader(''.join([unvst, '\\instructors.txt']), 3, '	')
gra = file_reader(''.join([unvst, '\\grades.txt']), 4, '	')

# Create dictionary for storing information of everyone
stus = defaultdict(Tuple[str, str, dict])
inss = defaultdict(Tuple[str, str, dict])

for cwid, name, dpt in stu:
    stus.setdefault(cwid, (name, dpt, dict()))

for cwid, name, dpt in ins:
    inss.setdefault(cwid, (name, dpt, dict()))

for sid, course, grade, iid in gra:
    try:
        stus[sid][2].setdefault(course, grade)
        if course not in inss[iid][2]:
            inss[iid][2].setdefault(course, 0)
        inss[iid][2][course] += 1
    except KeyError:
        print("ERROR!!!")
        print("There is some line in grades.txt that got an error.")
        raise SystemExit

# Turn dictionary to list
st: List[Students] = []
it: List[Instructors] = []

for cwid, lat in stus.items():
    S: Students = Students(cwid, lat[0], lat[1])
    S.set_cg(lat[2])
    st.append(S)

for cwid, lat in inss.items():
    I: Instructors = Instructors(cwid, lat[0], lat[1])
    I.set_co(lat[2])
    it.append(I)

uni.set_stu(st)
uni.set_ins(it)
uni.ptprint()
