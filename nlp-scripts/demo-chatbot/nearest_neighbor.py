#######################################
#Nearest neighbor classification in scikit-learn
from sklearn.metrics.pairwise 
import cosine_similarity

test_message = " i would like to find a flight from charlotte to las vegas that makes a stop in st. louis" 
test_x = nlp(test_message).vector 
scores = [ cosine_similarity(X[i,:], test_x) for i in range(len(sentences_train) ]
labels_train[np.argmax(scores)]

#######################################
# SVM/SVC: support vector machine/classifier
from sklearn.svm import SVC

clf = SVC()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

#######################################
# Intent classification with sklearn

# Import SVC
from sklearn.svm import SVC
# X_train and y_train was given.

# Create a support vector classifier
clf = SVC(C=1)

# Fit the classifier using the training data
clf.fit(X_train, y_train)

# Predict the labels of the test set
y_pred = clf.predict(X_test)

# Count the number of correct predictions
n_correct = 0
for i in range(len(y_test)):
    if y_pred[i] == y_test[i]:
        n_correct += 1

print("Predicted {0} correctly out of {1} test examples".format(n_correct, len(y_test)))