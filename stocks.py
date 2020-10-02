import os
import pandas as pd

index = 0
files = os.listdir("stocks/")
for i in range(len(files)):
    files[i] = "stocks/" + files[i]

stock = pd.read_csv(files[index])
closingPrices = stock["Close Price"]
print(stock.shape)
print(stock.keys())


def next_stock():
    global index, files, stock, closingPrices
    if index < len(files) - 1:
        index += 1
        stock = pd.read_csv(files[index])
        closingPrices = stock["Close Price"]
        return True
    else:
        return False


def get_name():
    return files[index].split(".")[0]
