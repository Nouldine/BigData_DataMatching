
import pandas as pd
import recordlinkage as rl
from recordlinkage.preprocessing import clean
import csv
import numpy as np
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

# This function is used to associate
# the records from the data frames 
# dfA and dfB
# @param1: dfA that is the first the csv Data Frame 
# @param2: dfB that is the second the csv Data Frame
# @param#: dfmatches that the set of matches from both data frames ( dfA, dfB ) 

def ShowMatching( dfA, dfB, dfmatches ):

    # Create a pan.das dataFrome  Object
    newDF = pd.DataFrame()
    
    # loop through the dfmatches dataset 
    # to associate them to the rigth 
    # dataset table according to their 
    # indexes 
    for row in dfmatches.iterrows():
        
        # indexed the second data frame
        # that will generate the indexes
        # using to_dict() function 
        # from the pandas library 
        indexA = row[ 0 ][ 0 ] 
        DictA = dfA.loc[indexA].to_dict()
        
        # indexed the second data frame
        # that will generate the indexes
        # using to_dict() function 
        # from the pandas library 
        indexB = row[ 0 ][ 1 ]
        DictB = dfB.loc[indexB].to_dict()
    
        newDict = {}

        # if the record is from the first dataFrame
        # associate B to the name of record Attributes 
        for item in DictA:

            col_name = "A_" + item 

            newDict[ col_name ] = DictA[ item ]

        # if the record is from the second dataFrame
        # associate B to the name of record attributes
        for item in DictB: 

            col_name = "B_" + item

            newDict[ col_name ] = DictB[ item ] 
        
      
        newSeries = newDict

        #  appended the names of the attributes to appropriate 
        #  column 
        newDF = newDF.append( newSeries, ignore_index = True ) 

    return newDF

# This function is used to do  the blocking and maching
# using the record linking library using the appropriate
# algorithm when both tables are passed

def blockingMatching():

    # first csv tables with the appropriate encoding 
    dfA = pd.read_csv("all_gamestop.csv",  encoding = 'utf-8' )

    # Second csv  table with the appropriate encoding
    dfB = pd.read_csv("jnl_half_edit2.csv",  encoding = 'utf-8')

    # effectuate the blocking on the "title" column 
    # because it is the column where the likelyhood 
    # of matching needs to be determined
    block_class = rl.BlockIndex( on = "title" )

    # Used function from the recordlinkage library 
    # to index the blocks ["title"] from both 
    # tables 
    condidate_links = block_class.index( dfA, dfB )

    #  Used the Compare() function 
    #  from the recordlinkage library 
    #  to effectuate the comparison
    compare = rl.Compare()

    # Do the first comparison with the string comparison. Knowing that 
    # the string structure may differ the edit distance algorithm (jarawinkler)
    # is used witht threshold of 0.85 
    compare.string("title", "title", method = 'jarowinkler', threshold = 0.85,  label = "Title")

    # knowing that the console structure  will be the same in both 
    # sets we compare the strings with the exact method 
    compare.exact('console', 'console', label = "Console")

    # Now we have both sets of record compute them to find 
    # the mathches using the compute() function from the
    # recordlinkage library. Storing the result in a vector
    compare_vectors = compare.compute( condidate_links, dfA, dfB )

    # Try try put records that belong to the same  entity together
    matches = compare_vectors[ compare_vectors.sum( axis = 1 ) > 1 ]


    # Called the showMaching function to assemble
    # the matches in the same set
    match_records = ShowMatching( dfA, dfB, matches ) 

    # Write the matches in csv file 
    np.savetxt("Matching.csv", match_records, delimiter = ",", fmt = "%s, %s, %s, %s, %s, %s, %s, %s" )

    # Get the matches indexes from the matche vector 
    df2 = pd.DataFrame( matches ) 
    
    # Put the indexes in a csv file  
    df2.to_csv("index_of_matching.csv")



# call the blockingMatching function 
# to finish the work 
blockingMatching()









