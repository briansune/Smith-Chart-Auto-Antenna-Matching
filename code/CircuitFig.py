from schemdraw import Drawing, ImageFormat
import schemdraw.elements as elm


class CircuitFig:

    def __init__(self, afm_c: str, stage: int, ser_shu_f: bool,
                 shu_an_t: chr, ser0_t: chr, shu_chp_t: chr,
                 shu_an: str = '', ser0: str = '', shu_chp: str = '', final_z: str = '50+0j'):

        self.image_data = None
        self.d = Drawing()
        self.afm_c = afm_c

        self.stage = stage
        self.ser_shu_f = ser_shu_f

        self.shu_an = self.ser0 = self.shu_chp = ''

        self.shu_an_t = {'r': elm.Capacitor(),
                         'l': elm.Inductor(),
                         'c': elm.Capacitor()}[shu_an_t]
        self.ser0_t = {'r': elm.Capacitor(),
                       'l': elm.Inductor(),
                       'c': elm.Capacitor()}[ser0_t]
        self.shu_chp_t = {'r': elm.Capacitor(),
                          'l': elm.Inductor(),
                          'c': elm.Capacitor()}[shu_chp_t]

        if self.stage >= 1 and not self.ser_shu_f:
            self.shu_an = shu_an
        if self.stage >= 2 or self.ser_shu_f:
            self.ser0 = ser0
        if self.stage >= 3 or self.ser_shu_f:
            self.shu_chp = shu_chp

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
