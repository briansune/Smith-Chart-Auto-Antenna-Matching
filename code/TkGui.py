# from skrf.data import ring_slot
from skrf import Network
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import CircuitFig
from PIL import ImageTk, Image
import io
# import MatchCal


class TkGui:

    def __init__(self, master):
        self.master = master
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(side=tk.LEFT)
        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.LEFT)

        # MatchCal.MatchCal()

        self.fig = Figure(figsize=(5, 6), dpi=100)
        self.fig_cvs = FigureCanvasTkAgg(self.fig, master=self.top_frame)
        self.ax = self.fig.gca()
        self.fig_cvs.get_tk_widget().pack(side=tk.LEFT)

        try:
            with open('ring slot.s1p', 'r') as f:
                pass
        except IOError:
            with open('ring slot.s1p', 'a+') as wf:
                wf.write("""!Created with skrf (http://scikit-rf.org).
        # GHz S RI R 50.0
        !freq ReS11 ImS11
        75.0 -0.503723180993 0.457844804761""")

        self.my_slot = Network('ring slot.s1p')

        self.plt_z0 = np.array([[[50+0j]]])
        self.plt_freq = 2.45e9
        self.fig2gui(np.array([[[50-50j]]]), 'To Match', 'r', 's')
        self.fig2gui(np.array([[[50+50j]]]), 'After Match', 'b', 'o')
        self.fig2gui(np.array([[[50-50j]]]), 'After Match', 'y', 'o')
        self.fig2gui(np.array([[[74+84j]]]), 'After Match', 'g', 'o')
        self.fig2gui(np.array([[[24-24j]]]), 'After Match', 'orange', 'o')

        crcfg = CircuitFig.CircuitFig('b', 1, False, 'c', 'l', 'c', '3pF')
        image = Image.open(io.BytesIO(crcfg.image_data)).resize((300, 180), Image.ANTIALIAS)
        self.conv2img = ImageTk.PhotoImage(image)

        self.lb1 = tk.Label(self.right_frame)
        self.lb1.image = self.conv2img
        self.lb1.configure(image=self.conv2img)
        self.lb1.grid(row=0, column=0)

        crcfg2 = CircuitFig.CircuitFig('y', 1, True, 'c', 'l', 'c', '', '8nH')
        image = Image.open(io.BytesIO(crcfg2.image_data)).resize((300, 180), Image.ANTIALIAS)
        self.conv2img = ImageTk.PhotoImage(image)

        self.lb2 = tk.Label(self.right_frame)
        self.lb2.image = self.conv2img
        self.lb2.configure(image=self.conv2img)
        self.lb2.grid(row=0, column=1)

        crcfg3 = CircuitFig.CircuitFig('g', 2, False, 'c', 'l', 'c', '12pF', '14nH', '')
        image = Image.open(io.BytesIO(crcfg3.image_data)).resize((300, 180), Image.ANTIALIAS)
        self.conv2img = ImageTk.PhotoImage(image)

        self.lb3 = tk.Label(self.right_frame)
        self.lb3.image = self.conv2img
        self.lb3.configure(image=self.conv2img)
        self.lb3.grid(row=1, column=0)

        crcfg4 = CircuitFig.CircuitFig('orange', 2, True, 'c', 'l', 'c', '', '7nH', '2pF')
        image = Image.open(io.BytesIO(crcfg4.image_data)).resize((300, 180), Image.ANTIALIAS)
        self.conv2img = ImageTk.PhotoImage(image)

        self.lb4 = tk.Label(self.right_frame)
        self.lb4.image = self.conv2img
        self.lb4.configure(image=self.conv2img)
        self.lb4.grid(row=1, column=1)

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
