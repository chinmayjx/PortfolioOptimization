import os
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt


class StockGUI:
    def __init__(self, name):
        if not os.path.exists("appdata"):
            os.mkdir("appdata")

        if not os.path.exists("appdata/" + name + ".csv"):
            file = open("appdata/" + name + ".csv", "w+")
            file.writelines(["key,value\n", "p,1\n", "d,1\n", "q,1\n"])
            file.close()
        self.app_data = pd.read_csv("appdata/" + name + ".csv", index_col=0).value

        # window config ###############################################################

        self.win = tk.Tk()
        self.screen_height = self.win.winfo_screenheight()
        self.screen_width = self.win.winfo_screenwidth()
        self.name = name
        self.win.title(self.name)
        self.win.minsize(int(self.screen_width / 5), int(self.screen_height / 7))

        # --------------------------------

        pdq = tk.Entry(self.win)
        pdq.configure(justify=tk.CENTER)
        pdq.insert(0, "p d q")
        pdq.pack()

        # ---------------------------------

        def list_click(w):
            if lb.get(lb.curselection()) == "plot":
                self.pldt()

        lb = tk.Listbox(self.win)
        lb.configure(justify=tk.CENTER)
        lb.bind("<Double-1>", list_click)
        fns = ["plot"]
        for x in fns:
            lb.insert(tk.END, x)
        lb.pack()

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


# StockGUI("reliance")
