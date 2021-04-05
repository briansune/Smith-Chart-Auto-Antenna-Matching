from math import pi, sqrt


class MatchCal:

    def __init__(self):
        self.tar_freq: float = 2e9
        self.ser: float = 0
        self.ser_t: chr = 'c'
        self.shu: float = 0
        self.shu_t: chr = 'c'

    def clear(self):
        self.ser: float = 0
        self.ser_t: chr = 'c'
        self.shu: float = 0
        self.shu_t: chr = 'c'

    def ser_0_sol(self, in_c: complex):
        img_v = in_c.imag

        if img_v > 0:
            self.ser_t: chr = 'c'
            self.ser = 1 / (2 * pi * self.tar_freq * img_v)
        else:
            self.ser_t: chr = 'l'
            self.ser = abs(img_v) / (2 * pi * self.tar_freq)

    def shu_0_sol(self, in_c: complex):
        z = (in_c.real ** 2 + in_c.imag ** 2) / in_c.imag
        if z > 0:
            self.shu_t: chr = 'c'
            self.shu = 1 / (2 * pi * self.tar_freq * z)
        else:
            self.shu_t: chr = 'l'
            self.shu = abs(z) / (2 * pi * self.tar_freq)

    def shu_50_sol(self, in_c: complex):
        a = 50 - in_c.real
        b = 100 * in_c.imag
        c = 50 * (in_c.real ** 2 + in_c.imag ** 2)

        d = (b ** 2) - (4 * a * c)
        sol1 = (-b - sqrt(d)) / (2 * a)
        sol2 = (-b + sqrt(d)) / (2 * a)

        if sol1 < 0 and sol2 < 0:
            self.shu = (max(sol1, sol2))
            self.shu_t: chr = 'c'
        elif sol1 >= 0 and sol2 >= 0:
            self.shu = (min(sol1, sol2))
            self.shu_t: chr = 'l'
        else:
            if in_c.imag >= 0:
                self.shu = (min(sol1, sol2))
                self.shu_t: chr = 'c'
            else:
                self.shu = (max(sol1, sol2))
                self.shu_t: chr = 'l'
