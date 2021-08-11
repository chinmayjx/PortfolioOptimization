import tkinter as tk

import pandas
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.stats import norm
import math
import pdf

matplotlib.rcParams["lines.linewidth"] = 0.5


class MarGui:
    def __init__(self, name):
        self.name = name
        self.btnct = 0
        self.curr_slab = None
        self.pdf1 = pdf.PDF("pdf/transition_" + name + ".pdf")

    def launch(self):
        name = self.name

        def prm_slab(nm, default):
            mk_slab = tk.Frame(win)
            mk_slab.pack(pady=10)
            self.curr_slab = mk_slab
            mk_plt = tk.Label(mk_slab, text=nm)
            mk_plt.pack(side=tk.LEFT, padx=20)

            mk_p = tk.Entry(mk_slab)
            mk_p.insert(0, default)
            mk_p.pack(side=tk.LEFT)
            return mk_p

        def mk_btn(nm, cmd=None):
            if self.btnct % 2 == 0:
                mk_slab = tk.Frame(win)
                mk_slab.pack(pady=10)
                self.curr_slab = mk_slab

            btn = tk.Button(self.curr_slab, text=nm, command=cmd)
            btn.pack(side=tk.LEFT)
            self.btnct += 1
            return btn

        df = pd.read_csv("stkdata/" + self.name + ".csv")
        ts = df["Close Price"].dropna().to_numpy()

        # window config ###############################################################
        win = tk.Tk()
        screen_height = win.winfo_screenheight()
        screen_width = win.winfo_screenwidth()
        name = name
        win.title(name)
        win.minsize(int(screen_width / 5), int(screen_height / 7))
    #     self.work(ts)
    # def work(self, ts):
        # methods #####################################################################
        def get_mav():
            nonlocal mav_array
            mav_array = data.rolling(mav_days).mean()
            for i in range(mav_days - 1):
                mav_array[i] = mav_array[mav_days - 1]

        def get_per_diff():
            nonlocal per_diff, brackets
            per_diff = pd.Series(index=index, dtype=float)
            brackets = pd.Series(index=index, dtype=float)
            for i in index:
                per_diff[i] = ((data[i] - mav_array[i]) * 100) / (abs(data[i]) + 1)
                brackets[i] = get_br(per_diff[i])

        def get_br(v):
            bb = bracket_bound
            v = math.floor(v + 0.5)
            if v > bb:
                v = bb
            if v < -1 * bb:
                v = -1 * bb
            return int(v)

        def get_transition_count():
            nonlocal transition_count, transition_prob
            idx = range(-1 * bracket_bound, bracket_bound + 1)
            transition_count = pd.DataFrame(0, index=idx, columns=idx, dtype=int)
            transition_prob = pd.DataFrame(0, index=idx, columns=idx, dtype=float)
            tfi = pd.Series(0, index=idx)
            for i in index[1:]:
                transition_count[brackets[i]][brackets[i - 1]] += 1
                tfi[brackets[i - 1]] += 1
            for i in idx:
                for j in idx:
                    if (tfi[i] == 0): continue
                    transition_prob[j][i] = transition_count[j][i] / tfi[i]

            for i in range(jump - 1):
                transition_prob = transition_prob.dot(transition_prob)

            # for i in idx:
            #     sm = 0.0
            #     for j in idx:
            #         sm += transition_prob[j][i]
            #     print(sm)

        def plot_mat(x):
            sns.heatmap(x)
            plt.show()

        def fit_normals():
            nonlocal normal_fits
            idx = range(-1 * bracket_bound, bracket_bound + 1)
            normal_fits = pd.DataFrame(0, index=[0, 1], columns=idx, dtype=float)
            for i in idx:
                dt = []
                for j in idx:
                    dt += [j] * int(100 * transition_prob[j][i])
                dt = np.array(dt)
                if len(dt) == 0:
                    continue
                normal_fits[i][0] = np.mean(dt)
                normal_fits[i][1] = np.std(dt)

        # variables ###################################################################
        name = self.name
        percent_train_data = 0.5
        bracket_bound = 20
        jump = 1
        mav_days = 30
        test_begin_index = int(percent_train_data * len(ts))
        data = pandas.Series(ts, dtype=float)
        index = data.index
        train = data[:test_begin_index]
        train_index = train.index
        test = data[test_begin_index:]
        test_index = test.index

        mav_array = None
        get_mav()

        per_diff = None
        brackets = None
        get_per_diff()

        transition_count = None
        transition_prob = None
        get_transition_count()
        # print(transition_count.to_string())

        normal_fits = None
        fit_normals()
        # print(normal_fits)

        # plot_mat(transition_prob)
        # plt.plot(data)
        # plt.plot(train)
        # plt.plot(test)
        # plt.plot(mav_array)
        # plt.show()
        # plt.plot(per_diff)
        # plt.plot(brackets)
        # plt.show()

        # ui ######################################################
        def plot_m():
            plt.plot(train)
            plt.plot(test)
            plt.show()
        plot_btn = mk_btn("plot",plot_m)

        def ptm():
            plot_mat(transition_prob)
        plot_transition_prob = mk_btn("plot transition matrix", ptm)
        win.mainloop()


nm = "TCS"
# nm = "ASTRAZEN"
MarGui(nm).launch()

# import stocks
# MarGui(nm).work(stocks.get_by_name(nm))
