import unittest
from HW10_Chengyi_Zhang import file_reader, read_sts, read_maj, read_ins


class MyTestCase(unittest.TestCase):
    def test_fr(self):
        """ Test file_reader """
        file = 'HW08_FR.txt'
        fs = open(file, 'w+')
        print('01|James|M\n02|George|M\n03|Marry|F', file=fs)
        k = 0
        exp = [('01', 'James', 'M'), ('02', 'George', 'M'), ('03', 'Marry', 'F')]
        for id, name, gender in file_reader(file, 3, sep='|', header=True):
            self.assertEqual(id, exp[k][0])
            self.assertEqual(name, exp[k][1])
            self.assertEqual(gender, exp[k][2])
            k += 1
        fs.close()

    def test_rs(self):
        # Test read_sts
        s = (("10101", 'Nick', 'Math'), ('10102', 'Jack', 'CS'))
        g = (("10101", 'MA500', 'A', '98765'), ('10102', 'CS550', 'B', '98080'))
        ans = read_sts(s, g)
        self.assertEqual(ans[0]._cg['MA500'], 'A')
        self.assertEqual(ans[0]._name, 'Nick')

    def test_ri(self):
        # Test read_ins
        g = (("10101", 'MA500', 'A', '98765'), ('10102', 'CS550', 'B', '98080'))
        i = (('98765', 'Harris', 'Math'), ('98080', 'Luis', 'CS'))
        ans = read_ins(i, g)
        self.assertEqual(ans[0]._name, 'Harris')
        self.assertEqual(ans[1]._name, 'Luis')

    def test_rm(self):
        # Test read_maj
        m = (('Math', 'R', 'MA500'), ('CS', 'E', 'CS550'))
        ans = read_maj(m)
        self.assertEqual(len(ans[0]._Courses), 1)
        self.assertEqual(len(ans[1]._Courses), 1)


if __name__ == '__main__':
    unittest.main()
