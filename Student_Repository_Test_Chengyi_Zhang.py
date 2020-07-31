import unittest
import HW09_Chengyi_Zhang


class MyTestCase(unittest.TestCase):
    def setUp(self):
        0

    def test_fr(self):
        """ Test file_reader """
        file = 'HW08_FR.txt'
        fs = open(file, 'w+')
        print('01|James|M\n02|George|M\n03|Marry|F', file=fs)
        k = 0
        exp = [('01', 'James', 'M'), ('02', 'George', 'M'), ('03', 'Marry', 'F')]
        for id, name, gender in HW09_Chengyi_Zhang.file_reader(file, 3, sep='|', header=True):
            self.assertEqual(id, exp[k][0])
            self.assertEqual(name, exp[k][1])
            self.assertEqual(gender, exp[k][2])
            k += 1
        fs.close()


if __name__ == '__main__':
    unittest.main()
