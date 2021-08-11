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
                per_diff[i] = ((data[i] - mav_array[i]) * 100) / (abs(mav_array[i]) + 1)
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

        def make_pred():
            nonlocal predictions, pred_per_dev
            predictions = pd.Series(index=index, dtype=float)
            pred_per_dev = pd.Series(index=index, dtype=float)
            for i in range(jump):
                predictions[i] = data[i]
                pred_per_dev[i] = brackets[i]

            for i in range(jump, len(data)):
                pb = brackets[i - jump]
                rd = np.random.normal(normal_fits[pb][0], normal_fits[pb][1])
                if rd < -1 * bracket_bound:
                    rd = -1 * bracket_bound
                if rd > bracket_bound:
                    rd = bracket_bound

                pred_per_dev[i] = rd
                predictions[i] = (rd/100)*(abs(mav_array[i])+1)+mav_array[i]

        # variables ###################################################################
        name = self.name
        percent_train_data = 0.5
        bracket_bound = 15
        jump = 10
        mav_days = 25

        if name == "TCS":
            bracket_bound = 15
            jump = 5
            mav_days = 12

        if name == "ASTRAZEN":
            bracket_bound = 15
            jump = 10
            mav_days = 12

        print(bracket_bound, jump, mav_days)

        test_begin_index = int(percent_train_data * len(ts))
        data = pandas.Series(ts, dtype=float)
        index = data.index
        train = data[:test_begin_index]
        train_index = train.index
        test = data[test_begin_index:]
        test_index = test.index

        mav_array = pd.Series(dtype=float)
        get_mav()

        per_diff = pd.Series(dtype=float)
        brackets = pd.Series(dtype=float)
        get_per_diff()

        transition_count = pd.DataFrame(dtype=float)
        transition_prob = pd.DataFrame(dtype=float)
        get_transition_count()
        print(transition_count.to_string())

        normal_fits = pd.DataFrame(dtype=float)
        fit_normals()

        predictions = pd.Series(dtype=float)
        pred_per_dev = pd.Series(dtype=float)
        make_pred()

        per_pred_stats = []
        pred_stats = []
        for i in index:
            dff = abs(predictions[i]-data[i])
            pred_stats.append(dff)
            per_pred_stats.append((dff*100)/data[i])

        # ui ######################################################
        def plot_m():
            plt.plot(train)
            plt.plot(test)
            plt.plot(mav_array)
            plt.show()

        plot_btn = mk_btn("plot", plot_m)

        def ptm():
            plot_mat(transition_prob)

        plot_transition_prob = mk_btn("plot transition matrix", ptm)

        def plt_norm():
            idx = range(-bracket_bound, bracket_bound + 1)
            for i in idx:
                plt.title("transitions from bracket " + str(i))
                plt.bar(idx, transition_prob.loc[i])
                plt.plot(idx, norm.pdf(idx, normal_fits[i][0], normal_fits[i][1]), color='red')
                self.pdf1.add()
                plt.clf()
            self.pdf1.save()

        pnf = mk_btn("plot normals", plt_norm)

        def stdst_plt():
            idx = range(-bracket_bound, bracket_bound + 1)
            plt.bar(idx, transition_prob.loc[0])
            plt.plot(idx, norm.pdf(idx, normal_fits[0][0], normal_fits[0][1]), color='red')
            plt.show()

        stdst_btn = mk_btn("steady state prob", stdst_plt)

        def pred_st():
            fig, ax = plt.subplots(ncols=2, figsize=(40, 20))
            ax[0].hist(per_pred_stats, bins=100)
            ax[1].hist(pred_stats, bins=100)
            plt.show()
        pred_btn = mk_btn("pred stats", pred_st)
        win.mainloop()


nm = "TCS"
# nm = "ASTRAZEN"
MarGui(nm).launch()
