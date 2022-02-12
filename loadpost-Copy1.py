import pandas as pd

df = pd.read_csv(r'C:\Users\19033\PycharmProjects\Analysis\Delta8_Reddit_Data\query1.csv',  encoding_errors='ignore')

for i in df['Post ID']:
    print(i)