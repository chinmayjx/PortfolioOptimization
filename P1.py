import pandas as pd
import matplotlib.pyplot as plt
import cvr
import stocks
import pdf

def frm(s):
    s = str(s)
    while len(s) < 8:
        s += " "
    return s


while True:
    c = cvr.Cover(stocks.stock["Close Price"], 30)
    x = list()
    y = list()
    while c.move_forward():
        # print(frm(c.min) + " " + frm(c.max) + " " + c.get_cover())
        x.append((c.curr - c.min) / (c.max - c.min))
        y.append(c.delta)

    plt.scatter(x, y, s=2)
    pdf.s(plt)

    if not stocks.next_stock():
        break
