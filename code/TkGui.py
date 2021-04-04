from skrf.data import ring_slot
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import CircuitFig
from PIL import ImageTk, Image
import io
import matplotlib


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

    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    canvas = FigureCanvasTkAgg(fig2plt, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT)


class TkGui:

    def __init__(self, master):
        self.master = master
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(side=tk.LEFT)
        self.next_frame = tk.Frame(self.master)
        self.next_frame.pack(side=tk.LEFT)
        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.LEFT)

        self.fig = Figure(figsize=(8, 5), dpi=100)

        z0 = np.array([[[50+0j]]])
        plt_d = np.array([[[50+50j]]])
        fig2gui(self.top_frame, self.fig, 2.45e9, z0, plt_d)

        matplotlib.use('agg')
        crcfg = CircuitFig.CircuitFig(1, False, 'c', 'l', 'c', '3pF')
        image = Image.open(io.BytesIO(crcfg.image_data))
        self.conv2img = ImageTk.PhotoImage(image)

        self.lb = tk.Label(self.next_frame)
        self.lb.image = self.conv2img
        self.lb.configure(image=self.conv2img)
        self.lb.pack(side=tk.TOP)

        crcfg2 = CircuitFig.CircuitFig(1, True, 'c', 'l', 'c', '', '8nH')
        image = Image.open(io.BytesIO(crcfg2.image_data))
        self.conv2img = ImageTk.PhotoImage(image)

        self.lb2 = tk.Label(self.next_frame)
        self.lb2.image = self.conv2img
        self.lb2.configure(image=self.conv2img)
        self.lb2.pack(side=tk.TOP)

        crcfg3 = CircuitFig.CircuitFig(2, False, 'c', 'l', 'c', '12pF', '14nH', '')
        image = Image.open(io.BytesIO(crcfg3.image_data))
        self.conv2img = ImageTk.PhotoImage(image)

        self.lb3 = tk.Label(self.right_frame)
        self.lb3.image = self.conv2img
        self.lb3.configure(image=self.conv2img)
        self.lb3.pack(side=tk.TOP)

        crcfg4 = CircuitFig.CircuitFig(2, True, 'c', 'l', 'c', '', '7nH', '2pF')
        image = Image.open(io.BytesIO(crcfg4.image_data))
        self.conv2img = ImageTk.PhotoImage(image)

        self.lb4 = tk.Label(self.right_frame)
        self.lb4.image = self.conv2img
        self.lb4.configure(image=self.conv2img)
        self.lb4.pack(side=tk.TOP)
