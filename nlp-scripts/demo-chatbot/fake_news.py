#######################################
#   CountVectorizer for text classification

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# head of df
print(df.head())

# series to store the labels
y = df.label

# training and test sets
X_train, X_test, y_train, y_test = train_test_split(df['text'], y, test_size=0.33, random_state=53)

#  CountVectorizer object
count_vectorizer = CountVectorizer(stop_words='english')

# transform training data using only the 'text' column values
count_train = count_vectorizer.fit_transform(X_train)

# transform the test data using only the 'text' column values
count_test = count_vectorizer.transform(X_test)

# first 10 features of the count_vectorizer
print(count_vectorizer.get_feature_names()[:10])

#######################################
#   TfidfVectorizer for text classification

from sklearn.feature_extraction.text import TfidfVectorizer

# TfidfVectorizer object
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)

# transform training data
tfidf_train = tfidf_vectorizer.fit_transform(X_train)

# transform test data
tfidf_test = tfidf_vectorizer.transform(X_test)

# first 10 features
print(tfidf_vectorizer.get_feature_names()[:10])

# first 5 vectors of tfidf training data
print(tfidf_train.A[:5])

#######################################
# Inspecting Vectors

# CountVectorizer DataFrame
count_df = pd.DataFrame(count_train.A, columns=count_vectorizer.get_feature_names())

# TfidfVectorizer DataFrame
tfidf_df = pd.DataFrame(tfidf_train.A, columns=tfidf_vectorizer.get_feature_names())

# head of count_df
print(count_df.head())

# head of tfidf_df
print(tfidf_df.head())

# Cdifference in columns
difference = set(count_df.columns) - set(tfidf_df.columns)
print(difference)

# Check if DataFrames are equal
print(count_df.equals(tfidf_df))

#######################################
# Training and testing the "fake news" model with CountVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

# Multinomial Naive Bayes classifier
nb_classifier = MultinomialNB()

# Fit classifier to training data
nb_classifier.fit(count_train, y_train)

# Create predicted tags
pred = nb_classifier.predict(count_test)

# Calculate accuracy score
score = metrics.accuracy_score(y_test, pred)
print(score)

# Calculate confusion matrix
cm = metrics.confusion_matrix(y_test, pred, labels=['FAKE', 'REAL'])
print(cm)

#######################################
#   Training and testing the "fake news" model with TfidfVectorizer

# Multinomial Naive Bayes classifier: nb_classifier
nb_classifier = MultinomialNB()

# Fit classifier to training data
nb_classifier.fit(tfidf_train, y_train)

# Create predicted tags
pred = nb_classifier.predict(tfidf_test)

# Calculate accuracy score
score = metrics.accuracy_score(y_test, pred)
print(score)

# Calculate confusion matrix: cm
cm = metrics.confusion_matrix(y_test, pred, labels=['FAKE', 'REAL'])
print(cm)

#######################################
#   Improving your model

# list of alphas
alphas = np.arange(0, 1, .1)

def train_and_predict(alpha):
    # classifier
    nb_classifier = MultinomialNB(alpha=alpha)
    # fit to training data
    nb_classifier.fit(tfidf_train, y_train)
    # predict labels
    pred = nb_classifier.predict(tfidf_test)
    # compute accuracy
    score = metrics.accuracy_score(y_test, pred)
    return score

# iterate alphas
for alpha in alphas:
    print('Alpha: ', alpha)
    print('Score: ', train_and_predict(alpha))
    print()

#######################################
#   Inspecting the model

# class labels
class_labels = nb_classifier.classes_

# extract features
feature_names = tfidf_vectorizer.get_feature_names()

# zip feature names with coefficient array and sort by weights
feat_with_weights = sorted(zip(nb_classifier.coef_[0], feature_names))

# first class label and top 20 feat_with_weights
print(class_labels[0], feat_with_weights[:20])

# second class label and bottom 20 feat_with_weights 
print(class_labels[1], feat_with_weights[-20:])
