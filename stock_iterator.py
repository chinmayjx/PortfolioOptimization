import stocks

def iterate(x):
    while True:
        x(stocks.closingPrices)
        if not stocks.next_stock():
            break
