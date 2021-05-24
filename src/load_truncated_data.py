import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds


train = tfds.load("cnn_dailymail", split="train[0:20000]")
validation = tfds.load("cnn_dailymail", split="validation[0:3000]")
test = tfds.load("cnn_dailymail", split="test[0:5000]")

train_df = tfds.as_dataframe(train)
validation_df = tfds.as_dataframe(validation)
test_df = tfds.as_dataframe(validation)

# Decoding bytes to string in pandas in both columns

def bytes_to_str(dataframe):
  '''
  Takes a dataframe column and converts it into a proper string
  '''
  dataframe['article'] = dataframe['article'].str.decode("utf-8")
  dataframe['highlights'] = dataframe['highlights'].str.decode("utf-8")
  return dataframe


if __name__ == "__main__":

    # Create a list of dataframes and convert byte data to string
    df_list = [train_df, test_df,validation_df]

    for dframe in df_list:
        dframe = bytes_to_str(dframe)

    # Save datasets
    train_df.to_csv("./data/raw/cnn_train.csv", index = False)
    validation_df.to_csv("./data/raw/cnn_validation.csv", index = False)
    test_df.to_csv("./data/raw/cnn_test.csv", index = False)
