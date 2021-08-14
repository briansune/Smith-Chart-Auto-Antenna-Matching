from math import pi, sqrt


def z_cal(freq: float, z_in: float, norm_c: float, norm_l: float) -> list:
    if z_in < 0:
        tmp_z = 1 / (2 * pi * freq * abs(z_in)) * norm_c
        tmp_t = 'c'
    else:
        tmp_z = z_in / (2 * pi * freq) * norm_l
        tmp_t = 'l'
    return [tmp_z, tmp_t]


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
        self.sol_valid = False

    def clear(self):
        self.ser = 0
        self.ser_t = 'c'
        self.shu = 0
        self.shu_t = 'c'
        self.tmp_z = 0
        self.sol_valid = False

    def ser_0_sol(self, in_c: complex):
        img_v = in_c.imag

        if in_c.imag == 0:
            self.tmp_z = in_c
            self.sol_valid = True if 48 < in_c.real < 52 else False
            return

        if img_v > 0:
            self.tmp_z = in_c - (img_v * 1j)
            self.ser_t: chr = 'c'
            self.ser = 1 / (2 * pi * self.tar_freq * img_v) * self.cap_base
        else:
            self.tmp_z = in_c - (img_v * 1j)
            self.ser_t: chr = 'l'
            self.ser = abs(img_v) / (2 * pi * self.tar_freq) * self.ind_base
        self.sol_valid = True if 48 < self.tmp_z.real < 52 else False

    def shu_0_sol(self, in_c: complex):
        if in_c.imag == 0:
            self.tmp_z = in_c
            self.sol_valid = True if 48 < in_c.real < 52 else False
            return
        z = (in_c.real ** 2 + in_c.imag ** 2) / in_c.imag
        if z > 0:
            self.tmp_z = in_c * (-z * 1j) / (in_c + (-z * 1j))
            self.shu_t: chr = 'c'
            self.shu = 1 / (2 * pi * self.tar_freq * z) * self.cap_base
        else:
            self.tmp_z = in_c * (abs(z) * 1j) / (in_c + (abs(z) * 1j))
            self.shu_t: chr = 'l'
            self.shu = abs(z) / (2 * pi * self.tar_freq) * self.ind_base
        self.sol_valid = True if 48 < self.tmp_z.real < 52 else False

    def shu_50_sol(self, in_c: complex, ans_sel: bool = False):

        a = 50 - in_c.real
        b = 100 * in_c.imag
        c = 50 * (in_c.real ** 2 + in_c.imag ** 2)
        if in_c.imag == 0 or a == 0:
            self.tmp_z = in_c
            return

        d = (b ** 2) - (4 * a * c)
        if d < 0:
            self.tmp_z = in_c
            self.sol_valid = False
            return

        if ans_sel:
            sol = (-b - sqrt(d)) / (2 * a)
        else:
            sol = (-b + sqrt(d)) / (2 * a)

        [self.shu, self.shu_t] = z_cal(self.tar_freq, sol, self.cap_base, self.ind_base)
        tmp = 1j * sol
        self.tmp_z = (in_c * tmp) / (in_c + tmp)
        self.sol_valid = True if 48 < self.tmp_z.real < 52 else False

    def ser_50_sol(self, in_c: complex, ans_sel: bool = False):
        rel_v = in_c.real
        img_v = in_c.imag

        real_v = rel_v / 0.02 - rel_v ** 2

        a = 1
        b = 2 * img_v
        c = img_v ** 2 - real_v
        d = (b ** 2) - (4 * a * c)

        if d < 0:
            self.tmp_z = in_c
            self.sol_valid = False
            return

        if ans_sel:
            sol = (-b - sqrt(d)) / (2 * a)
        else:
            sol = (-b + sqrt(d)) / (2 * a)

        [self.ser, self.ser_t] = z_cal(self.tar_freq, sol, self.cap_base, self.ind_base)
        self.tmp_z = in_c.real + (in_c.imag + sol) * 1j
        self.sol_valid = True if 48 < self.tmp_z.real < 52 else False

    def sol_2stage(self, in_c: complex, shu_ser_f: bool = False, ans_sel: bool = False):
        if in_c.imag == 0:
            self.tmp_z = in_c
            return
        self.clear()
        if shu_ser_f:
            self.shu_50_sol(in_c, ans_sel)
            self.ser_0_sol(self.tmp_z)
        else:
            self.ser_50_sol(in_c, ans_sel)
            self.shu_0_sol(self.tmp_z)
