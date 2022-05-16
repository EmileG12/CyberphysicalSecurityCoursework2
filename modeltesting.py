# https://stackabuse.com/overview-of-classification-methods-in-python-with-scikit-learn/
# Begin by importing all necessary libraries
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = pd.read_csv("support/TrainingData.txt", header=None)

# It is a good idea to check and make sure the data is loaded as expected.

print(data.head(5))


# # Pandas ".iloc" expects row_indexer, column_indexer
X = data.iloc[:, :-1].values
# # Now let's tell the dataframe which column we want for the target/labels.
y = data[24]
#print(X[:5])
#print(y[:5])
# # Test size specifies how much of the data you want to set aside for the testing set.
# # Random_state parameter is just a random seed we can use.
# # You can use it if you'd like to reproduce these specific results.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

print("testing the SVC model")
SVC_model = SVC()
# training
SVC_model.fit(X_train, y_train)
# prediction
print("X_test values: ")
print(X_test)
SVC_prediction = SVC_model.predict(X_test)
#  Accuracy score is the simplest way to evaluate
print("Accuracy score for SVC: ", accuracy_score(SVC_prediction, y_test))


print("testing the KNN model")

# KNN model requires you to specify n_neighbors,
# the number of points the classifier will look at to determine what class a new point belongs to
KNN_model = KNeighborsClassifier(n_neighbors=3)
# training
KNN_model.fit(X_train, y_train)
# prediction
KNN_prediction = KNN_model.predict(X_test)

print("Accuracy score for KNN: ", accuracy_score(KNN_prediction, y_test))

# But Confusion Matrix and Classification Report give more details about performance
# print(confusion_matrix(SVC_prediction, y_test))
# print(classification_report(KNN_prediction, y_test))
