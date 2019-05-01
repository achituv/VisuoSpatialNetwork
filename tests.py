from sklearn.neural_network import MLPClassifier



import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.svm import LinearSVC
import pandas as pd
from sklearn.metrics import scorer
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score



df = pd.read_excel(r'C:\Users\achituv\Desktop\ANN_input.xls') # data frame


input_df = df[df.columns[:11]]
output_df = df[df.columns[11:]]
# input_df = np.array([df.columns[:11]])
# output_df = np.array(df[df.columns[11:]])

train_x, test_x, train_y, test_y = train_test_split(input_df, output_df, test_size=0.2)


clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(train_x, train_y)

dat1 = clf.predict(test_x)
print (test_y.shape)
print (dat1.shape)
print(type(dat1))
print(type(test_y))
print(clf.score(np.array(test_x), np.array(test_y)))
print(clf.score(test_x, test_y))
# accuracy_score(np.array(test_y), dat1)f
print(clf.score(test_x, dat1))

accuracy_score(test_y, dat1)

# precision_score(y_true, y_pred, average=None)

#
# X = [[0., 0., 0, 0, 0], [1., 1., 1, 1, 1],[2., 2., 2, 2, 2],[3., 3., 3, 3, 3]]
# y = [[0], [1],[2], [3]]
# X1 = [[0., 0., 0, 0, 0], [2., 2., 2, 2, 2]]
# y1 = [[0], [1]]
# clf = MLPClassifier(activation='logistic', batch_size='auto',
#                     beta_1=0.9, beta_2=0.99, early_stopping=False,
#                     epsilon=1e-08, hidden_layer_sizes=(39, 40, 6), learning_rate='adaptive',
#                     learning_rate_init=0.1, max_iter=10000, momentum=0.9,
#                     nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
#                     solver='lbfgs', tol=0.000001, validation_fraction=0.1, verbose=False,
#                     warm_start=False)
#
# clf.fit(X,y )
# print(clf.score(X1,y1))
# print(clf.predict([[0.5, 0.5, 0.5, 0.5, 0.5]]))
