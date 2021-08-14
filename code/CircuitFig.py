from schemdraw import Drawing, ImageFormat
import schemdraw.elements as elm
from matplotlib import pyplot as plt


class CircuitFig:

    def __init__(self, afm_c: str, stage: int, ser_shu_f: bool,
                 cmp_l: list, cmp_v: list, final_z: str):

        self.image_data = None
        self.d = Drawing()
        self.afm_c = afm_c

        self.stage = stage
        self.ser_shu_f = ser_shu_f

        self.shu_an = self.ser0 = self.shu_chp = ''

        self.shu_an_t = {'r': elm.Resistor(),
                         'l': elm.Inductor(),
                         'c': elm.Capacitor()}[cmp_l[0]]
        self.ser0_t = {'r': elm.Resistor(),
                       'l': elm.Inductor(),
                       'c': elm.Capacitor()}[cmp_l[1]]
        self.shu_chp_t = {'r': elm.Resistor(),
                          'l': elm.Inductor(),
                          'c': elm.Capacitor()}[cmp_l[2]]

        if self.stage >= 1 and not self.ser_shu_f:
            self.shu_an = cmp_v[0]
        if self.stage >= 1 or self.ser_shu_f:
            self.ser0 = cmp_v[1]
        if self.stage >= 3 or self.ser_shu_f:
            self.shu_chp = cmp_v[2]

        self.final_z = final_z

        self.set4cv()
        self.up2img()

    def set4cv(self):
        self.d.add(elm.Antenna().label('ANT'))
        an_arw = self.d.add(elm.Line().left())
        self.d.add(elm.CurrentLabelInline(direction='out').at(an_arw)).color('r')
        self.d.add(elm.Dot())
        self.d.push()
        self.d.add(self.shu_an_t.down().label(self.shu_an))
        self.d.add(elm.Ground())
        self.d.pop()
        self.d.add(self.ser0_t.left().label(self.ser0))
        self.d.add(elm.Dot())
        self.d.push()
        self.d.add(self.shu_chp_t.down().label(self.shu_chp))
        self.d.add(elm.Ground())
        self.d.pop()
        lk2 = self.d.add(elm.Line().left())
        self.d.add(elm.CurrentLabel().at(lk2).right().label(f'{self.final_z} Ω')).color(self.afm_c)
        self.up2img()

    def up2img(self):
        self.d.draw(show=False)
        self.image_data = self.d.get_imagedata(ImageFormat.PNG)
        plt.close(plt.gcf())
