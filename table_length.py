
import pandas as pd
import recordlinkage as rl
from recordlinkage.preprocessing import clean
import csv
import numpy as np
import sys


def table_length():

    # first csv tables with the appropriate encoding 
    dfA = pd.read_csv("all_gamestop.csv",  encoding = 'utf-8' )

    # Second csv  table with the appropriate encoding
    dfB = pd.read_csv("jnl_half_edit2.csv",  encoding = 'utf-8')
    
    #dfC = pd.read_csv("Matching.csv", encoding = 'utf-8' )
    
    indexer =  rl.BlockIndex(on='title')

    pairs = indexer.index( dfA, dfB )


    print("DataFrame1:", len( dfA ) ) 

    print("DataFrame2:", len( dfB ) ) 

    print("Pair: ", len( pairs )  )

    #print("Matches: ", len( dfC ) ) 



table_length()
