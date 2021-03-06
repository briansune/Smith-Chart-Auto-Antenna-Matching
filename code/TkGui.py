import skrf
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import CircuitFig
from PIL import ImageTk, Image, ImageDraw
import io
import MatchCal


l2z = lambda l: l[0] + 1j * l[1]
s4cmp = lambda sf: 'nH' if sf == 'l' else 'pF'


def ld4img2gui(label: tk.Label,
               color: str, stage: int, sh_se: bool,
               cmp_l: list, cmp_v: list, z_val: str = '50+0j',
               valid: bool = True):
    cr_cfg = CircuitFig.CircuitFig(color, stage, sh_se, cmp_l, cmp_v, z_val)
    image = Image.open(io.BytesIO(cr_cfg.image_data)).resize((300, 180), Image.ANTIALIAS)

    im = Image.new('RGBA', (300, 180), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    im.paste(image, (0, 0))
    if not valid:
        draw.line((0, 0, 300, 180), fill=(255, 0, 0, 255), width=5)
        draw.line((0, 180, 300, 0), fill=(255, 0, 0, 255), width=5)
    label.image = ImageTk.PhotoImage(im)

    label.configure(image=label.image)


class TkGui:

    def __init__(self, master):
        self.master = master
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(side=tk.LEFT)
        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.upper_sch_f = tk.Frame(self.right_frame)
        self.upper_sch_f.grid(row=0, padx=(0, 5), pady=(5, 0), sticky="nsew")
        self.lower_ety_f = tk.Frame(self.right_frame)
        self.lower_ety_f.grid(row=1, padx=(0, 5), pady=(0, 5), sticky="nsew")

        self.fig = Figure(figsize=(5, 6), dpi=100)
        self.fig_cvs = FigureCanvasTkAgg(self.fig, master=self.top_frame)
        self.ax: Figure = self.fig.gca()
        self.fig_cvs.get_tk_widget().pack(side=tk.LEFT, padx=5, pady=5)

        try:
            with open('ring slot.s1p', 'r'):
                pass
        except IOError:
            with open('ring slot.s1p', 'a+') as wf:
                wf.write("""!Created with skrf (http://scikit-rf.org).
        # GHz S RI R 50.0
        !freq ReS11 ImS11
        75.0 -0.503723180993 0.457844804761""")

        self.my_slot = skrf.Network('ring slot.s1p')

        self.to_match_z = [50, 0]
        self.ser_match_z = [50, 0]
        self.shu_match_z = [50, 0]
        self.shu_ser_match_z_a = [50, 0]
        self.shu_ser_match_z_b = [50, 0]
        self.ser_shu_match_z_a = [50, 0]
        self.ser_shu_match_z_b = [50, 0]
        self.plt_z0 = 50 + 0j
        self.plt_freq = 2.45e9
        self.up2chart()

        self.lb1 = tk.Label(self.upper_sch_f, relief="ridge")
        self.lb1_tit = tk.Label(
            self.upper_sch_f, text='Shunt Matching', relief="raised").grid(
            row=0, column=0, sticky="nsew")
        self.lb1.grid(row=1, column=0)

        self.lb2 = tk.Label(self.upper_sch_f, relief="ridge")
        self.lb2_tit = tk.Label(
            self.upper_sch_f, text='Series Matching', relief="raised").grid(
            row=0, column=1, sticky="nsew")
        self.lb2.grid(row=1, column=1)

        self.lb3 = tk.Label(self.upper_sch_f, relief="ridge")
        self.lb3_tit = tk.Label(
            self.upper_sch_f, text='Shunt-Series Matching', relief="raised").grid(
            row=2, column=0, sticky="nsew")
        self.lb3.grid(row=3, column=0)

        self.lb4 = tk.Label(self.upper_sch_f, relief="ridge")
        self.lb4_tit = tk.Label(
            self.upper_sch_f, text='Shunt-Series Matching', relief="raised").grid(
            row=2, column=1, sticky="nsew")
        self.lb4.grid(row=3, column=1)

        self.lb5 = tk.Label(self.upper_sch_f, relief="ridge")
        self.lb5_tit = tk.Label(
            self.upper_sch_f, text='Series-Shunt Matching', relief="raised").grid(
            row=4, column=0, sticky="nsew")
        self.lb5.grid(row=5, column=0)

        self.lb6 = tk.Label(self.upper_sch_f, relief="ridge")
        self.lb6_tit = tk.Label(
            self.upper_sch_f, text='Series-Shunt Matching', relief="raised").grid(
            row=4, column=1, sticky="nsew")
        self.lb6.grid(row=5, column=1)

        ld4img2gui(self.lb1, 'b', 1, False, ['c', 'l', 'c'], ['NC', 'SHORT', ''])
        ld4img2gui(self.lb2, 'y', 1, True, ['c', 'l', 'c'], ['', 'SHORT', ''])
        ld4img2gui(self.lb3, 'g', 2, False, ['c', 'l', 'c'], ['NC', 'SHORT', ''])
        ld4img2gui(self.lb4, 'purple', 2, False, ['c', 'l', 'c'], ['NC', 'SHORT', ''])
        ld4img2gui(self.lb5, 'orange', 2, True, ['c', 'l', 'c'], ['', 'SHORT', 'NC'])
        ld4img2gui(self.lb6, 'brown', 2, True, ['c', 'l', 'c'], ['', 'SHORT', 'NC'])

        ###################################################################
        self.to_match_r = tk.StringVar(value=str(self.to_match_z[0]))
        self.to_match_i = tk.StringVar(value=str(self.to_match_z[1]))

        self.ety_lb1 = tk.Label(self.lower_ety_f, text='To Match Complex Value')
        self.ety_lb1.pack(side=tk.TOP)
        self.ety_lb1b = tk.Label(self.lower_ety_f, text='Z = ')
        self.ety_lb1b.pack(side=tk.LEFT)
        self.ety1_r = tk.Entry(self.lower_ety_f, textvariable=self.to_match_r)
        self.ety1_r.pack(side=tk.LEFT)
        self.ety_lb1c = tk.Label(self.lower_ety_f, text=' + ')
        self.ety_lb1c.pack(side=tk.LEFT)
        self.ety1_i = tk.Entry(self.lower_ety_f, textvariable=self.to_match_i)
        self.ety1_i.pack(side=tk.LEFT)
        self.ety_lb1c = tk.Label(self.lower_ety_f, text='j')
        self.ety_lb1c.pack(side=tk.LEFT)

        self.enter = tk.Button(self.lower_ety_f, text="Start Auto Solver",
                               command=self.ld2chart)
        self.enter.pack(side=tk.LEFT)

    def ld2chart(self):
        self.to_match_z = [float(self.ety1_r.get()), float(self.ety1_i.get())]

        tmp_cal = MatchCal.MatchCal()
        tmp_cal.tar_freq = self.plt_freq
        to_mat = float(self.ety1_r.get()) + 1j * float(self.ety1_i.get())

        tmp_cal.shu_0_sol(to_mat)
        disp_str = f'{tmp_cal.shu:.2f} {s4cmp(tmp_cal.shu_t)}' if tmp_cal.shu else 'NC'
        ld4img2gui(self.lb1, 'b', 1, False, [tmp_cal.shu_t, 'l', 'c'],
                   [disp_str, 'SHORT', ''],
                   f'{int(tmp_cal.tmp_z.real)}+{int(tmp_cal.tmp_z.imag)}j',
                   tmp_cal.sol_valid)
        self.ser_match_z = [tmp_cal.tmp_z.real, tmp_cal.tmp_z.imag]

        tmp_cal.ser_0_sol(to_mat)
        disp_str = f'{tmp_cal.ser:.2f} {s4cmp(tmp_cal.ser_t)}' if tmp_cal.ser else 'SHORT'
        ld4img2gui(self.lb2, 'y', 1, True, ['c', tmp_cal.ser_t, 'c'],
                   ['', disp_str, ''],
                   f'{int(tmp_cal.tmp_z.real)}+{int(tmp_cal.tmp_z.imag)}j',
                   tmp_cal.sol_valid)
        self.shu_match_z = [tmp_cal.tmp_z.real, tmp_cal.tmp_z.imag]

        tmp_cal.sol_2stage(to_mat, True)
        disp_str1 = f'{tmp_cal.ser:.2f} {s4cmp(tmp_cal.ser_t)}' if tmp_cal.ser else 'SHORT'
        disp_str2 = f'{tmp_cal.shu:.2f} {s4cmp(tmp_cal.shu_t)}' if tmp_cal.shu else 'NC'
        ld4img2gui(self.lb3, 'g', 2, False, [tmp_cal.shu_t, tmp_cal.ser_t, 'c'],
                   [disp_str2, disp_str1, ''],
                   f'{int(tmp_cal.tmp_z.real)}+{int(tmp_cal.tmp_z.imag)}j',
                   tmp_cal.sol_valid)
        self.shu_ser_match_z_a = [tmp_cal.tmp_z.real, tmp_cal.tmp_z.imag]

        tmp_cal.sol_2stage(to_mat, True, True)
        disp_str1 = f'{tmp_cal.ser:.2f} {s4cmp(tmp_cal.ser_t)}' if tmp_cal.ser else 'SHORT'
        disp_str2 = f'{tmp_cal.shu:.2f} {s4cmp(tmp_cal.shu_t)}' if tmp_cal.shu else 'NC'
        ld4img2gui(self.lb4, 'purple', 2, False, [tmp_cal.shu_t, tmp_cal.ser_t, 'c'],
                   [disp_str2, disp_str1, ''],
                   f'{int(tmp_cal.tmp_z.real)}+{int(tmp_cal.tmp_z.imag)}j',
                   tmp_cal.sol_valid)
        self.shu_ser_match_z_b = [tmp_cal.tmp_z.real, tmp_cal.tmp_z.imag]

        tmp_cal.sol_2stage(to_mat)
        disp_str1 = f'{tmp_cal.ser:.2f} {s4cmp(tmp_cal.ser_t)}' if tmp_cal.ser else 'SHORT'
        disp_str2 = f'{tmp_cal.shu:.2f} {s4cmp(tmp_cal.shu_t)}' if tmp_cal.shu else 'NC'
        ld4img2gui(self.lb5, 'orange', 2, True, ['c', tmp_cal.ser_t, tmp_cal.shu_t],
                   ['', disp_str1, disp_str2],
                   f'{int(tmp_cal.tmp_z.real)}+{int(tmp_cal.tmp_z.imag)}j',
                   tmp_cal.sol_valid)
        self.ser_shu_match_z_a = [tmp_cal.tmp_z.real, tmp_cal.tmp_z.imag]

        tmp_cal.sol_2stage(to_mat, ans_sel=True)
        disp_str1 = f'{tmp_cal.ser:.2f} {s4cmp(tmp_cal.ser_t)}' if tmp_cal.ser else 'SHORT'
        disp_str2 = f'{tmp_cal.shu:.2f} {s4cmp(tmp_cal.shu_t)}' if tmp_cal.shu else 'NC'
        ld4img2gui(self.lb6, 'brown', 2, True, ['c', tmp_cal.ser_t, tmp_cal.shu_t],
                   ['', disp_str1, disp_str2],
                   f'{int(tmp_cal.tmp_z.real)}+{int(tmp_cal.tmp_z.imag)}j',
                   tmp_cal.sol_valid)
        self.ser_shu_match_z_b = [tmp_cal.tmp_z.real, tmp_cal.tmp_z.imag]
        self.up2chart()

    def up2chart(self):
        self.ax.clear()
        self.fig2gui(np.array([[[l2z(self.to_match_z)]]]), 'To Match', 'r', 's')
        self.fig2gui(np.array([[[l2z(self.ser_match_z)]]]), 'After Match', 'b', 'o')
        self.fig2gui(np.array([[[l2z(self.shu_match_z)]]]), 'After Match', 'y', 'o')
        self.fig2gui(np.array([[[l2z(self.shu_ser_match_z_a)]]]), 'After Match', 'g', 'o')
        self.fig2gui(np.array([[[l2z(self.shu_ser_match_z_b)]]]), 'After Match', 'purple', 'o')
        self.fig2gui(np.array([[[l2z(self.ser_shu_match_z_a)]]]), 'After Match', 'orange', 'o')
        self.fig2gui(np.array([[[l2z(self.ser_shu_match_z_b)]]]), 'After Match', 'brown', 'o')

    def fig2gui(self, plt_data: np.array,
                label: str = '', color: str = 'r', mark: str = 's',
                plt_sel: bool = False) -> None:

        self.my_slot.frequency = self.plt_freq
        self.my_slot.z0 = self.plt_z0
        self.my_slot.z = plt_data

        if plt_sel:
            self.my_slot.plot_s_db(ax=self.ax)
        else:
            self.my_slot.plot_s_smith(ax=self.ax, draw_labels=True, show_legend=False,
                                      label=label, color=color, chart_type='zy', marker=mark)

        self.ax.legend(bbox_to_anchor=(0.5, 1.05), loc='lower center', ncol=3,
                       fancybox=True, shadow=True)
        self.fig_cvs.draw()
