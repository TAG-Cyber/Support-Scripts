import pandas as pd

data = pd.read_excel('C:\ Path to file \ file.xlsx')
df = pd.DataFrame(data)
df.groupby(df.columns.tolist(), as_index=False).size()
