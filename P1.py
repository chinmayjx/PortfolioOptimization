import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("reliance.csv")
print(df.shape)
print(df.keys())
# print(df["Close Price"])
plt.plot(df["Close Price"])
plt.show()