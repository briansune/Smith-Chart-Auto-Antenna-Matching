from skrf.data import ring_slot
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import CircuitFig
from PIL import ImageTk, Image
import io
import matplotlib
import MatchCal


def fig2gui(frame: tk.Frame, fig2plt: Figure,
            plt_freq: np.array, plt_z0: np.array,
            plt_data: np.array, plt_sel: bool = False) -> None:

    ring_slot.frequency = plt_freq
    # normalization
    ring_slot.z0 = plt_z0
    ring_slot.z = plt_data

    ax = fig2plt.gca()

    if plt_sel:
        ring_slot.plot_s_db(ax=ax)
    else:
        ring_slot.plot_s_smith(ax=ax, draw_labels=True, show_legend=False,
                               label='To Match', color='r',
                               chart_type='zy', marker='s')

        ring_slot.z = np.array([[[50-50j]]])
        ring_slot.plot_s_smith(ax=ax, draw_labels=True, show_legend=False,
                               label='After Match', color='b',
                               chart_type='zy', marker='o')
        ring_slot.z = np.array([[[50 + 20j]]])
        ring_slot.plot_s_smith(ax=ax, draw_labels=True, show_legend=False,
                               label='After Match', color='y',
                               chart_type='zy', marker='o')
        ring_slot.z = np.array([[[50 + 80j]]])
        ring_slot.plot_s_smith(ax=ax, draw_labels=True, show_legend=False,
                               label='After Match', color='g',
                               chart_type='zy', marker='o')
        ring_slot.z = np.array([[[20 - 30j]]])
        ring_slot.plot_s_smith(ax=ax, draw_labels=True, show_legend=False,
                               label='After Match', color='orange',
                               chart_type='zy', marker='o')

    ax.legend(bbox_to_anchor=(0.5, 1.05), loc='lower center', ncol=3,
              fancybox=True, shadow=True)

    canvas = FigureCanvasTkAgg(fig2plt, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT)


class TkGui:

    def __init__(self, master):
        self.master = master
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(side=tk.LEFT)
        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.LEFT)

        MatchCal.MatchCal()

        self.fig = Figure(figsize=(5, 6), dpi=100)

        z0 = np.array([[[50+0j]]])
        plt_d = np.array([[[50+50j]]])
        fig2gui(self.top_frame, self.fig, 2.45e9, z0, plt_d)

        matplotlib.use('agg')
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
