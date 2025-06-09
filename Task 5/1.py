import pandas as pd

# Load the Titanic dataset
train_df = pd.read_csv("/mnt/data/train.csv")
test_df = pd.read_csv("/mnt/data/test.csv")
gender_submission_df = pd.read_csv("/mnt/data/gender_submission.csv")

# Show basic structure and summary
train_info = train_df.info()
train_description = train_df.describe()
train_head = train_df.head()

train_info, train_description, train_head
