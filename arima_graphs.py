import stocks
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
import pdf
import pandas as pd

"""
1. Iterate on stocks.
2. Create a function analyse for timeseries analysis.
3. analyse() uses a function to predict p,q,d and other function to generate the forecast data

"""

pr = pdf.PDF("pdf/arima321.pdf", True)


def predict_pdq(ts):
    return 3, 2, 1


def add_graphs():
    pass


# def analyse(ts):
#     model = ARIMA(ts, order=predict_pdq(ts))
#     model_fit = model.fit(disp=0)
#     # print(model_fit.summary())
#     model_fit.plot_predict(dynamic=False, ax=plt.gca())
#     plt.title(stocks.get_name().split(".")[0].split("/")[1])
#     # plt.show()
#     pr.add()


def analyze(ts, f):
    train = ts[:int(len(ts) * f)]
    test = ts[int(len(ts) * f):]
    model = ARIMA(train, predict_pdq(ts))
    model_fit = model.fit(disp=-1)
    plt.plot(test)
    plt.plot(train)

    an = pd.Series(model_fit.forecast(len(ts) - int(len(ts) * f), alpha=0.05)[0], index=test.index)
    plt.plot(an)
    model_fit.plot_predict(start=int(len(ts) * f), end=int(len(ts) * 1.2), dynamic=False, ax=plt.gca())
    plt.title(stocks.get_name().split(".")[0].split("/")[1])
    pr.add()


while True:
    analyze(stocks.stock["Close Price"], 0.6)
    if not stocks.next_stock():
        break

pr.save()
