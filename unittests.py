import unittest
from random import randint
from main import *

class TestEmployee(unittest.TestCase):

    def test_transport_route_01(self):

        st1 = Station(1, "Львів", 49.948726, 24.543115)
        st2 = Station(2, "Київ", 50.921909, 30.731047)

        ps1 = ("Vitaliy", 20, st1.title, st2.title)
        ps2 = ("Oleg", 21, st1.title, st2.title)
        ps3 = ("Illya", 22, st1.title, st2.title)
        ps4 = ("Dima", 23, st1.title, st2.title)

        all_ps = [ps1, ps2, ps3, ps4]

        tran1 = Bus(len(all_ps), 4500, 200, "Grugoriy")

        a = Route()
        a.route_calculation(tran1, st1, st2, all_ps)

    def test_transport_route_02(self):

        st1 = Station(4, "Одеса", 46.290872, 30.443615)
        st2 = Station(5, "Тернопіль", 49.342179, 25.368033)

        ps1 = ("Taras", 123, st1.title, st2.title)
        ps2 = ("Anton", 124, st1.title, st2.title)
        ps3 = ("Vitaliy", 125, st1.title, st2.title)
        ps4 = ("Viktoria", 126, st1.title, st2.title)
        ps5 = ("Kateryna", 127, st1.title, st2.title)
        ps6 = ("Ostap", 128, st1.title, st2.title)
        ps7 = ("Stepan", 129, st1.title, st2.title)
        ps8 = ("Ystum", 130, st1.title, st2.title)

        all_ps = [ps1, ps2, ps3, ps4, ps5, ps6, ps7, ps8]

        tran1 = Train(len(all_ps), 15500, 1500, "Vasya")

        a = Route()
        a.route_calculation(tran1, st1, st2, all_ps)
    
    def test_transport_route_03(self):

        st1 = Station(1, "Львів", 49.948726, 24.543115)
        st2 = Station(8, "Херсон", 46.382479, 32.365233)

        ps1 = ("Taras", 10, st1.title, st2.title)
        ps2 = ("Anton", 11, st1.title, st2.title)
        ps3 = ("Vitaliy", 12, st1.title, st2.title)
        ps4 = ("Mariya", 13, st1.title, st2.title)

        all_ps = [ps1, ps2, ps3, ps4]

        tran1 = Truck(len(all_ps), 2500, 235, "Liolik")

        a = Route()
        a.route_calculation(tran1, st1, st2, all_ps)


if __name__ == '__main__':
    unittest.main()