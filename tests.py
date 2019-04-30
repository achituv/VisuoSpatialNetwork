from sklearn.neural_network import MLPClassifier

X = [[0., 0., 0.5, 0.2, 0.5], [1., 1., 0.8, 0.2, 0.1]]
y = [[2], [3]]
X1 = [[0., 0., 0.5, 0.2, 0.5], [1., 1., 0.8, 0.2, 0.1]]
y1 = [[2], [4]]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)

clf.fit(X,y )
print(clf.score(X1,y1))
print(clf.predict([[1., 2., 0.8, 0.5, 0.7]]))
