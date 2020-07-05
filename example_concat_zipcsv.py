
import pandas as pd
import zipfile

def openByDate(zipfpath, startdate, enddate):
    '''
    open zip and read files within the range of the starting date and ending date
    preferable, controllable
    '''
    dfs = []
    with zipfile.ZipFile(zipfpath) as z:     #   z.infolist()
        filenames = [f.filename for f in z.infolist()]
        for d in pd.date_range(startdate, enddate, freq='D'):
            toOpen = 'Rulo_5SW/Rulo_5SW_soil_{:%Y%m%d}_0703.csv'.format(d)
            if toOpen in filenames:
                # check if the file exists in the zip
                with z.open(toOpen) as f:
                    dfs.append(pd.read_csv(f, header=0, skiprows=1).iloc[2:])
    return pd.concat(dfs).reset_index(drop=True)


def openAllExisting(zipfpath):
    '''
    passively open all files. may open some files you don't want and make cleaning up more difficult
    '''
    
    soil = []
    agl = []
    with zipfile.ZipFile(zipfpath) as z:     #   
        for f in z.infolist():
            fname = f.filename
            if fname.endswith('csv'):
                # check if it is a CSV file then open it
                with z.open(fname) as f:
                    df = pd.read_csv(f, header=0, skiprows=1).iloc[2:]
                if 'soil' in fname:
                    soil.append(df)
                if 'agl' in fname:
                    agl.append(df)

    return pd.concat(agl).reset_index(drop=True), pd.concat(soil).reset_index(drop=True)


soil = openByDate('F:/Downloads/Compressed/Rulo_5SW.zip', '2019-06-19', '2020-06-30')


agl, soil2 = openAllExisting('F:/Downloads/Compressed/Rulo_5SW.zip')
