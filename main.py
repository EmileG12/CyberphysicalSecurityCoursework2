# https://stackabuse.com/overview-of-classification-methods-in-python-with-scikit-learn/
# Begin by importing all necessary libraries
import pandas
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from scheduler import compute_schedule_user_energy_demand
from scheduler import userconstraints
from matplotlib import pyplot as plt

data = pd.read_csv("support/TrainingData.txt", header=None)
print("training data : ")
training_data = pd.read_csv("support/TrainingData.txt", header=None)
print(training_data)
print("Testing data: ")
testing_data = pd.read_csv("support/TestingData.txt", header=None)
print(testing_data)
# It is a good idea to check and make sure the data is loaded as expected.

# # Pandas ".iloc" expects row_indexer, column_indexer
# # Now let's tell the dataframe which column we want for the target/labels.
#print(X[:5])
#print(y[:5])
# # Test size specifies how much of the data you want to set aside for the testing set.
# # Random_state parameter is just a random seed we can use.
# # You can use it if you'd like to reproduce these specific results.
x_training = training_data.iloc[:, :-1]
y_training = training_data.iloc[:, -1:]

print("testing the SVC model")
SVC_model = SVC()
# training
SVC_model.fit(x_training, y_training)
# prediction

SVC_prediction = SVC_model.predict(testing_data)
print("SVCPredictions: ")
print(SVC_prediction)

testingframe = pandas.DataFrame(SVC_prediction, columns=["normal"])
testedframe = pandas.concat([testing_data,testingframe], axis=1)
print(testedframe)
abnormalframe = testedframe.loc[testedframe['normal'] == 1]
print("abnormalframe: ")
abnormalframe = abnormalframe.iloc[:, :-1]
print(abnormalframe.values.tolist())
guidelines = abnormalframe.values.tolist()
schedules = []
for guideline in guidelines:
    schedules.append(compute_schedule_user_energy_demand(userconstraints,price_guideline=guideline))

for schedule in schedules:
    print("Schedule: " + str(schedule))


