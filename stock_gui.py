import os
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA


def arima_man_forecast(ts, f, order, name):
    train = ts[:int(len(ts) * f)]
    test = ts[int(len(ts) * f):]
    model = ARIMA(train, order)
    model_fit = model.fit(disp=-1)
    plt.plot(test)
    plt.plot(train)

    # an = pd.Series(model_fit.forecast(len(ts) - int(len(ts) * f), alpha=0.05)[0], index=test.index)
    # plt.plot(an)
    model_fit.plot_predict(start=int(len(ts) * f), end=int(len(ts) * 1.2), dynamic=False, ax=plt.gca())
    plt.title(name + " | [p,d,q] : " + str(order))
    plt.show()


def arima_insample(ts, g, order, name):
    model = ARIMA(ts, order)
    fit = model.fit(disp=-1)
    p = pd.Series(dtype=float)
    print(type(fit))
    if g == 1:
        p = fit.predict(typ="levels")
    else:
        i = int(0.1*len(ts))
        while i < ts.index[-1]:
            p = p.append(fit.predict(start=i, end=i + g - 1, dynamic=True, typ="levels"))
            i += g
    plt.plot(ts)
    plt.plot(p)
    plt.title(name + " | [p,d,q] : " + str(order)+" | gap="+str(g))
    plt.show()


class StockGUI:
    def __init__(self, name):
        if not os.path.exists("appdata"):
            os.mkdir("appdata")

        if not os.path.exists("appdata/" + name + ".csv"):
            file = open("appdata/" + name + ".csv", "w+")
            file.writelines(["key,value\n", "p,1\n", "d,1\n", "q,1\n", "f,0.5\n", "g,1\n"])
            file.close()
        self.app_data = pd.read_csv("appdata/" + name + ".csv", index_col=0).value
        self.p = int(self.app_data["p"])
        self.d = int(self.app_data["d"])
        self.q = int(self.app_data["q"])
        self.f = float(self.app_data["f"])
        self.g = int(self.app_data["g"])

        self.ts = pd.read_csv("stkdata/" + name + ".csv")["Close Price"]

        # window config ###############################################################

        self.win = tk.Tk()
        self.screen_height = self.win.winfo_screenheight()
        self.screen_width = self.win.winfo_screenwidth()
        self.name = name
        self.win.title(self.name)
        self.win.minsize(int(self.screen_width / 5), int(self.screen_height / 7))

        # ---------------------------------

        def plf():
            self.pldt()

        plt_btn = tk.Button(self.win, text="plot", command=plf)
        plt_btn.pack()

        # --------------------------------

        lbl_arima_start = tk.Label(self.win, text="------------ ARIMA ------------")
        lbl_arima_start.pack()
        self.arima_params = ["p", "d", "q", "f", "g"]

        pdq_frame = tk.Frame(self.win)
        pdq_frame.pack()

        pdq = tk.Entry(pdq_frame)
        pdq.configure(justify=tk.CENTER)
        pdq.insert(0, "(p,d,q) : " + str(int(self.p)) + "," + str(int(self.d)) + "," + str(int(self.q)))

        pdq.pack(side=tk.LEFT)

        # --------------------------------

        def call_arima_forecast():
            tp = [1, 1, 1]
            i = 0
            for x in str(pdq.get().split(":")[1]).strip().split(","):
                tp[i] = int(x)
                i += 1
            arima_man_forecast(self.ts, float(fraction.get().split(":")[1].strip()), tp, self.name)

        forecast_tab = tk.Frame(self.win)
        forecast_tab.pack(pady=(10,0))

        fraction = tk.Entry(forecast_tab)
        fraction.insert(0, "(train%) : " + str(self.f))
        fraction.pack(side=tk.LEFT)

        forecast_btn = tk.Button(forecast_tab, text="forecast ", command=call_arima_forecast)
        forecast_btn.pack(side=tk.LEFT, padx=20)

        # --------------------------------

        def call_arima_insample():
            tp = [1, 1, 1]
            i = 0
            for x in str(pdq.get().split(":")[1]).strip().split(","):
                tp[i] = int(x)
                i += 1
            arima_insample(self.ts, int(gap.get().split(":")[1].strip()), tp, self.name)

        insample_tab = tk.Frame(self.win)
        insample_tab.pack(pady=(0,10))

        gap = tk.Entry(insample_tab)
        gap.insert(0, "(gap) : " + str(int(self.g)))
        gap.pack(side=tk.LEFT)

        insample_btn = tk.Button(insample_tab, text="insample", command=call_arima_insample)
        insample_btn.pack(side=tk.LEFT, padx=20)

        # --------------------------------

        def iter_params():
            for x in self.app_data.keys():
                setattr(self, x, self.app_data[x])

        def update_params():
            tp = str(pdq.get().split(":")[1]).strip().split(",")
            if len(tp) == 3:
                self.app_data["p"] = tp[0]
                self.app_data["d"] = tp[1]
                self.app_data["q"] = tp[2]
                print(tp)
            self.app_data["f"] = fraction.get().split(":")[1].strip()
            self.app_data["g"] = gap.get().split(":")[1].strip()
            iter_params()
            self.app_data.to_csv("appdata/" + name + ".csv")

        def reset_params():
            pdq.delete(0, 'end')
            pdq.insert(0, "(p,d,q) : " + str(int(self.p)) + "," + str(int(self.d)) + "," + str(int(self.q)))
            fraction.delete(0, 'end')
            fraction.insert(0, "(train%) : " + str(self.f))
            gap.delete(0, 'end')
            gap.insert(0, "(gap) : " + str(int(self.g)))

        reset_save = tk.Frame(self.win)
        reset = tk.Button(reset_save, text="  reset boxes  ", command=reset_params)
        update = tk.Button(reset_save, text="update params", command=update_params)
        reset.pack(side=tk.LEFT)
        update.pack(side=tk.LEFT)
        reset_save.pack()

        lbl_arima_end = tk.Label(self.win, text="-------------------------------")
        lbl_arima_end.pack()

        ################################################################################

        self.df = pd.read_csv("stkdata/" + self.name + ".csv")
        self.ts = self.df["Close Price"]
        print(self.df.head)

    def pldt(self):
        plt.plot(self.ts)
        plt.title(self.name)
        plt.xlabel("Index")
        plt.ylabel("Price")
        plt.show()

    def launch(self):
        self.win.mainloop()


# arima_insample(pd.read_csv("ignore/AirPassengers.csv")["Close Price"], 4, (3, 1, 1))
