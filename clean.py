import pandas as pd
import sys
filename = sys.argv[1]

df = pd.read_csv(filename)
df.drop_duplicates(subset ="video_id",keep = 'first', inplace = True)
df.to_csv(filename[0:-4]+"2.csv",index=False)
