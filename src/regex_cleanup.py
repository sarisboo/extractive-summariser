import pandas as pd 
import re

# Compose concatenated regex expression to clean data faster 
start_of_string = "^\s*"
remove_cnn = '.*\((CNN|EW.com)\)?(\s+--\s+)?'
remove_by_1 = 'By \.([^.*]+\.)?([^.]*\. PUBLISHED: \.[^|]*\| \.)? UPDATED:[^.]+\.[^.]+\.\s*'
remove_by_2 = 'By \.([^.*]+\.)?(\sand[^.*]+\.\s*)?(UPDATED[^.*]+\.[^.*]+\.\s*)?(\slast[^.*]+\.\s*)?'
remove_last_updated = 'Last[^.*]+\.\s'
remove_twitter_link = 'By \.([^.*]+\.)\s*Follow\s@@[^.*]+\.\s+'
remove_published = '(PUBLISHED[^.*]+\.[^.*]+\.[^.*]+\.\s*)(UPDATED[^.*]+\.[^.*]+\.\s*)?'
# end_of_string = '[\'"]*\s*$'

r_cleanup_source = \
  start_of_string +\
  "(" +\
    "|".join([
      remove_cnn,
      remove_by_1,
      remove_by_2,
      remove_last_updated,
      remove_twitter_link,
      remove_published,
    ]) +\
  ")"

r_cleanup = re.compile(r_cleanup_source)

def cleanup(text):
  # todo replace using r_cleanup
  return r_cleanup.sub('', text)

# Clean and select highlights columns

# Removes newline characters
r_remove_newline_charcter = re.compile('\\n')
def remove_newline(text):
  return r_remove_newline_charcter.sub('', text)

# Removes punctuation -- NOT SURE ABOUT THIS!
r_remove_dot_charcter = re.compile('\.')
def remove_dot(text):
  return r_remove_dot_charcter.sub('', text)

# Remove '\xa0\' characters at the begining and end of each group
def find_and_replace_xa0(text):
    return re.sub('(\\xa0)',' ', text)

if __name__ == '__main__':
    # Read datasets 
    train = pd.read_csv('./data/raw/cnn_train.csv')
    test = pd.read_csv('./data/raw/cnn_test.csv')
    validation = pd.read_csv('./data/raw/cnn_validation.csv')

    # Copy datasets to not hurt raw data 
    train_copy = train.copy()
    test_copy = test.copy()
    validation_copy = validation.copy()
    
    # Apply the cleanup function to the article column
    train_copy.article = train_copy.article.apply(cleanup)
    test_copy.article = test_copy.article.apply(cleanup)
    validation_copy.article = validation_copy.article.apply(cleanup)
    
    print(train_copy.article.head())

    ## Create one big sentence as summary by removing newline and punctuation
    # Training set 
    train_copy.highlights =  train_copy.highlights.apply(remove_newline)
    #train_copy.highlights = train_copy.highlights.apply(remove_dot)
    # Validation set 
    validation_copy.highlights = validation_copy.highlights.apply(remove_newline)
    #validation_copy.highlights = validation_copy.highlights.apply(remove_dot)
    # Testing set 
    test_copy.highlights =  test_copy.highlights.apply(remove_newline)
    #test_copy.highlights =  test_copy.highlights.apply(remove_dot)
    
    print(train_copy.highlights.iloc[10])

    ## Remove characters at the starta and end of some words
    train_copy.article =  train_copy.article.apply(find_and_replace_xa0)
    train_copy.highlights =  train_copy.highlights.apply(find_and_replace_xa0)

    test_copy.article =  test_copy.article.apply(find_and_replace_xa0)
    test_copy.highlights =  test_copy.highlights.apply(find_and_replace_xa0)

    validation_copy.article =  validation_copy.article.apply(find_and_replace_xa0)
    validation_copy.highlights =  validation_copy.highlights.apply(find_and_replace_xa0)

    print(validation_copy.highlights.iloc[10])
    # Save datasets
    train_copy.to_csv("./data/cleaned/train_cleaned.csv", index = False)
    validation_copy.to_csv("./data/cleaned/validation_cleaned.csv", index = False)
    test_copy.to_csv("./data/cleaned/test_cleaned.csv", index = False)
    
