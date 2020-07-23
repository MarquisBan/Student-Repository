from prettytable import PrettyTable
from typing import List, Tuple
from collections import defaultdict
import itertools


# Dict Turning Grade to GPA
GPA = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75, 'C+': 2.25, 'C': 2.0}


class Students:
    def __init__(self, cwid: str, name: str, dpt: str):
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dpt
        self._cg: dict = {}
        self._gpa: float = 0

    def set_cg(self, courseandgrades: dict):
        self._cg = courseandgrades

    def calc_gpa(self) -> float:
        sum: float = 0
        num: int = 0
        for course, grade in self._cg.items():
            if grade in GPA:
                sum += GPA[grade]
                num += 1
            else:
                num += 1
        if num != 0:
            self._gpa = sum/num
            return self._gpa
        else:
            return 0


class Instructors:
    def __init__(self, cwid: str, name: str, dpt: str):
        self._cwid = cwid
        self._name = name
        self._dept = dpt
        self._course = {}

    def set_co(self, courseandstu: dict):
        self._course = courseandstu


class Major:
    def __init__(self, mname, courses: List[Tuple[str, bool]]):
        self._Name = mname
        self._Courses = courses
        self._required = [x[0] for x in self._Courses if x[1] == True]
        self._elective = [x[0] for x in self._Courses if x[1] == False]


class University:
    def __init__(self, name: str):
        self._name = name
        self._students: List[Students] = []
        self._instructors: List[Instructors] = []
        self._majors: List[Major] = []
        self._majdic: dict = {}

    def set_stu(self, stus: List[Students]):
        self._students = stus

    def set_ins(self, inss: List[Instructors]):
        self._instructors = inss

    def set_maj(self, majs: List[Major]):
        self._majors = majs
        self._majdic = dict()
        for one in majs:
            self._majdic.setdefault(one._Name, one)

    def ptprint(self) -> None:
        ptm = PrettyTable(['Major', 'Required Courses', 'Electives'])
        pts = PrettyTable(['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives', 'GPA'])
        pti = PrettyTable(['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for one in self._majors:
            ptm.add_row([one._Name, sorted(one._required), sorted(one._elective)])
        for one in self._students:
            try:
                major_req = self._majdic[one._dept]._required
                major_ele = self._majdic[one._dept]._elective
            except KeyError:
                print("ERROR!!!")
                print("There is no major '{}' in major list.".format(one._dept))
                raise SystemExit
            else:
                rem_req = list(set(major_req)-set(one._cg.keys()))
                rem_ele = list(set(major_ele)-set(one._cg.keys()))
                pts.add_row([one._cwid, one._name, one._dept, sorted(list(one._cg.keys())), rem_req, rem_ele, "%.2f" % one.calc_gpa()])
        for one in self._instructors:
            for course in one._course:
                pti.add_row([one._cwid, one._name, one._dept, course, one._course[course]])

        print("Majors Summary")
        print(ptm)
        print("Student Summary")
        print(pts)
        print("Instructor Summary")
        print(pti)


unvst: str = input("Please input the university name, which is also the name of directory: ")
# Build the instance of University
uni = University(unvst)


# file_reader from HW08
def file_reader(path: str, fields: int, sep=',', header=False):
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
stu = file_reader(''.join([unvst, '\\students.txt']), 3, ';', True)
ins = file_reader(''.join([unvst, '\\instructors.txt']), 3, '|', True)
gra = file_reader(''.join([unvst, '\\grades.txt']), 4, '|', True)
g1, g2, g3 = itertools.tee(gra, 3)
maj = file_reader(unvst + "\\majors.txt", 3, '\t', True)


# Extract Input Information to Each Class

def read_sts(stu, gra) -> List[Students]:
    stus = defaultdict(Tuple[str, str, dict])
    for cwid, name, dpt in stu:
        stus.setdefault(cwid, (name, dpt, dict()))
    for sid, course, grade, iid in gra:
        try:
            stus[sid][2].setdefault(course, grade)
        except KeyError:
            print("ERROR!!!")
            print("There is some line in grades.txt that got an error.")
            raise SystemExit
    ret = []
    for cwid, lat in stus.items():
        S: Students = Students(cwid, lat[0], lat[1])
        S.set_cg(lat[2])
        ret.append(S)
    return ret


def read_ins(ins, gra) -> List[Instructors]:
    inss = defaultdict(Tuple[str, str, dict])
    for cwid, name, dpt in ins:
        inss.setdefault(cwid, (name, dpt, dict()))
    for sid, course, grade, iid in gra:
        try:
            if course not in inss[iid][2]:
                inss[iid][2].setdefault(course, 0)
            inss[iid][2][course] += 1
        except KeyError:
            print("ERROR!!!")
            print("There is some line in grades.txt that got an error.")
            raise SystemExit
    ret = []
    for cwid, lat in inss.items():
        I: Instructors = Instructors(cwid, lat[0], lat[1])
        I.set_co(lat[2])
        ret.append(I)
    return ret


def read_maj(maj) -> List[Major]:
    majs = defaultdict(list)
    for mname, r, course in maj:
        if r == 'R':
            required = True
        elif r == 'E':
            required = False
        else:
            print("ERROR!!!")
            print("There is some line in majors.txt that got an error.")
            raise SystemExit
        majs[mname].append((course, required))
    ret = []
    for mname, lat in majs.items():
        M: Major = Major(mname, lat)
        ret.append(M)
    return ret


# Turn dictionary to list
st: List[Students] = read_sts(stu, g1)
it: List[Instructors] = read_ins(ins, g2)
mj: List[Major] = read_maj(maj)

# Turn information into uni(versity)
uni.set_stu(st)
uni.set_ins(it)
uni.set_maj(mj)
uni.ptprint()
