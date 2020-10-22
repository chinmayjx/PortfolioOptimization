import stocks
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
import pdf


pr = pdf.PDF("pdf/arimax.pdf",True)
while True:
    model = ARIMA(stocks.stock["Close Price"], order=(1, 1, 1))
    model_fit = model.fit(disp=0)
    # print(model_fit.summary())
    model_fit.plot_predict(dynamic=False,ax=plt.gca())
    plt.title(stocks.get_name().split(".")[0].split("/")[1])
    # plt.show()
    pr.add()
    if not stocks.next_stock():
        break

pr.save()