import pandas as pd

data = pd.read_excel('C:\ Path to File \ File.xlsx')
df = pd.DataFrame(data)


def colorcodes(x):
    h = x.copy()
    h['Dup'] = h.duplicate(keep=False)
    mask = h['Dup'] == True

    h.loo[mask, :] = 'background-color: orange'
    h.loo[~mask, :] = 'background-color: ""'
    return h.drop('Dup', axis=1)


df.style.apply(colorcodes, axis=None)
