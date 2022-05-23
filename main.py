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

print("training data : ")
training_data = pd.read_csv("support/TrainingData.txt", header=None)
print(training_data)
print("Testing data: ")
testing_data = pd.read_csv("support/TestingData.txt", header=None)
print(testing_data)
# It is a good idea to check and make sure the data is loaded as expected.

# # Pandas ".iloc" expects row_indexer, column_indexer
# # Now let's tell the dataframe which column we want for the target/labels.
# # Test size specifies how much of the data you want to set aside for the testing set.
# # Random_state parameter is just a random seed we can use.
# # You can use it if you'd like to reproduce these specific results.
x_training = training_data.iloc[:, :-1]
y_training = training_data.iloc[:, -1:]

print("Training the SVC Model")
SVC_model = SVC()
# training
SVC_model.fit(x_training, y_training)
# prediction

SVC_prediction = SVC_model.predict(testing_data)
print("SVCPredictions: ")
print(SVC_prediction)

# forming a panda DataFrame from the prediction, with only a single column containing each 1 or 0 label in order
testingframe = pandas.DataFrame(SVC_prediction, columns=["normal"])
# concatenate our results with the testing data, to get the testing data with each corresponding label
testedframe = pandas.concat([testing_data,testingframe], axis=1)
print(testedframe)
# Exporting the previous table to a Report txt file
testedframe.to_csv("Report.txt", header=False, index=False)

# get the testedframe and filter out normal priceguidelines from the tested data
abnormalframe = testedframe.loc[testedframe['normal'] == 1]

# remove the label from the filtered DataFrame so we can have all the abnormal price guidelines for scheduling
abnormalframe = abnormalframe.iloc[:, :-1]
guidelines = abnormalframe.values.tolist()
schedules = []
lpcounter = 0

#For each price guideline, produce an energy schedule using LP programming
# each of these schedules will be copied into the schedules list

for guideline in guidelines:
    schedules.append(compute_schedule_user_energy_demand(userconstraints,price_guideline=guideline,lpcounter=lpcounter))
    # variable used to count the number of schedules we've made and output a unique LP script
    # for each price guideline
    lpcounter= lpcounter+1

numberofcharts = 0
# For each schedule produce, create a graph and output it to a unique png
for schedule in schedules:
    plt.title("Energy schedule")
    plt.xlabel("Time")
    plt.ylabel("Energy demand")
    plt.bar(range(24), schedule)
    plt.savefig("energyschedulechart_" + str(numberofcharts))
    plt.close()
    plt.figure()
    numberofcharts = numberofcharts + 1


