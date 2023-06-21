import os
import pandas as pd
from sklearn.model_selection import train_test_split

def numerals_normalize( df ):

  for i in range(len(df)):
    words = df['Data'][i].split()
    st = ''
    for word in words:
      if(st != ''):
        st += ' '
      if(word[0]>='0' and word[0] <='9' and word[-1]>='0' and word[-1] <='9'):
        st += "CC"
      else:
        st += word
    df['Data'][i] = st

  return df
