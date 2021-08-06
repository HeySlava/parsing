import camelot
import pandas as pd

# Read pdf into list of DataFrame
table = camelot.read_pdf('./price.pdf', pages='1,2,3,4,5')
df = pd.DataFrame()

for i in range(5):
    print(df.append(table[i].df))
