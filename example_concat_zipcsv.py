
import pandas as pd
import zipfile

dfs = []
with zipfile.ZipFile('F:/Downloads/Compressed/Rulo_5SW.zip') as z:     #   z.infolist()
    for d in pd.date_range('2019-08-24', '2019-08-30', freq='D'):
        with z.open('Rulo_5SW/Rulo_5SW_soil_{:%Y%m%d}_0703.csv'.format(d)) as f:
            dfs.append(pd.read_csv(f, header=0, skiprows=1).iloc[2:])
        

df_all = pd.concat(dfs).reset_index(drop=True)
