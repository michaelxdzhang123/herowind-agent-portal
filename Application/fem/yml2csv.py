import pandas as pd
import yaml
from os import path ,getcwd
yml1 = path.join(getcwd(),"s123_v6.yml")
yml2 = path.join(getcwd(),"s123_lam_chg.yml")
allf = [yml1,yml2]
for file in allf:
    with open(path.join(getcwd(),file)) as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        df = pd.DataFrame(data)
        name,extension = file.split('.')
        sa_f = path.join(getcwd(),name+".csv")
        df.to_csv(sa_f,index=False)
