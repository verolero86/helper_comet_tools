#!/usr/bin/env python3

import pandas as pd
import numpy as np
import argparse

def read_leaf(fname):

    """
    Reads a CSV file containing spectra data from a single leaf image.
    """

    leaf_df = pd.read_csv(fname)

    print(leaf_df.shape)
    print(leaf_df)
    
    leaf_arr = leaf_df.to_numpy()
    print(leaf_arr.shape)

    # The provided CSV files have a pixel index, a row index, and a column
    # index
    labels_index = 3

    # Keep max_pixel number of pixels
    max_pixel = 10
    labels = leaf_arr[0:max_pixel,0:labels_index]
    values = leaf_arr[0:max_pixel,labels_index:]

    # Review collected values
    print(f"labels = {labels}")
    print(f"values.shape = {values.shape}")
    print(f"values = {values}")


    # Convert to column vectors
    vec_values = values.transpose()
    print(f"vec_values.shape = {vec_values.shape}")
    print(f"vec_values = {vec_values}")
    
    return vec_values


# Main program

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Preprocess leaf spectra data for CoMet.')
    parser.add_argument('--csvfile', required=True, help="The combined CSV file of a leaf spectra data.")
    parser.add_argument('--leafid', required=True, help="The unique ID for a single leaf.")
    args = parser.parse_args()
    #print(args)

    # Store arguments
    csvfile = args.csvfile
    leafid = args.leafid

    vectors = read_leaf(csvfile)

    np.savetxt(fname="vectors_"+leafid+".tsv",X=vectors,delimiter="\t",fmt='%s')

