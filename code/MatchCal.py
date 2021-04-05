from math import pi, sqrt


class MatchCal:

    def __init__(self):
        self.tar_freq: float = 2e9
        self.ser: float = 0
        self.ser_t: chr = 'c'
        self.shu: float = 0
        self.shu_t: chr = 'c'
        self.ind_base = 1e9
        self.cap_base = 1e12
        self.tmp_z: complex = 0

    def clear(self):
        self.ser = 0
        self.ser_t = 'c'
        self.shu = 0
        self.shu_t = 'c'
        self.tmp_z = 0

    def ser_0_sol(self, in_c: complex):
        img_v = in_c.imag

        if img_v > 0:
            self.tmp_z = in_c - (img_v * 1j)
            self.ser_t: chr = 'c'
            self.ser = 1 / (2 * pi * self.tar_freq * img_v) * self.cap_base
        else:
            self.tmp_z = in_c - (img_v * 1j)
            self.ser_t: chr = 'l'
            self.ser = abs(img_v) / (2 * pi * self.tar_freq) * self.ind_base

    def shu_0_sol(self, in_c: complex):
        z = (in_c.real ** 2 + in_c.imag ** 2) / in_c.imag
        if z > 0:
            self.tmp_z = in_c * (-z * 1j) / (in_c + (-z * 1j))
            self.shu_t: chr = 'c'
            self.shu = 1 / (2 * pi * self.tar_freq * z) * self.cap_base
        else:
            self.tmp_z = in_c * (abs(z) * 1j) / (in_c + (abs(z) * 1j))
            self.shu_t: chr = 'l'
            self.shu = abs(z) / (2 * pi * self.tar_freq) * self.ind_base

    def shu_50_sol(self, in_c: complex):
        a = 50 - in_c.real
        b = 100 * in_c.imag
        c = 50 * (in_c.real ** 2 + in_c.imag ** 2)

        d = (b ** 2) - (4 * a * c)
        sol1 = (-b - sqrt(d)) / (2 * a)
        sol2 = (-b + sqrt(d)) / (2 * a)

        if sol1 < 0 and sol2 < 0:
            tmp = (max(sol1, sol2))
            self.shu = 1 / (2 * pi * self.tar_freq * abs(tmp)) * self.cap_base
            self.shu_t: chr = 'c'
        elif sol1 >= 0 and sol2 >= 0:
            tmp = (min(sol1, sol2))
            self.shu = tmp / (2 * pi * self.tar_freq) * self.ind_base
            self.shu_t: chr = 'l'
        else:
            if in_c.imag >= 0:
                tmp = (min(sol1, sol2))
                self.shu = 1 / (2 * pi * self.tar_freq * abs(tmp)) * self.cap_base
                self.shu_t: chr = 'c'
            else:
                tmp = (max(sol1, sol2))
                self.shu = tmp / (2 * pi * self.tar_freq) * self.ind_base
                self.shu_t: chr = 'l'
        tmp = 1j*tmp
        self.tmp_z = (in_c * tmp) / (in_c + tmp)

    def ser_50_sol(self, in_c: complex):
        img_v = in_c.imag
        if img_v > 0:
            z_tar = img_v + 25
            self.ser_t: chr = 'c'
            self.ser = 1 / (2 * pi * self.tar_freq * z_tar) * self.cap_base
            self.tmp_z = in_c.real - 25j
        else:
            z_tar = 25 - img_v
            self.ser_t: chr = 'l'
            self.ser = z_tar / (2 * pi * self.tar_freq) * self.ind_base
            self.tmp_z = in_c.real + 25j

    def sol_2stage(self, in_c: complex, shu_ser_f: bool = False):
        self.clear()
        if shu_ser_f:
            self.shu_50_sol(in_c)
            self.ser_0_sol(self.tmp_z)
        else:
            self.ser_50_sol(in_c)
            self.shu_0_sol(self.tmp_z)
