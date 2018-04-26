from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


def check(clf, X_test, y_test):
    vls = clf.predict(X_test)
    print 'predict: ', vls
    print 'real: ', y_test
    plt.plot(vls)
    plt.plot(y_test)
    plt.show()
    print "mean square error: ", mean_squared_error(y_test, vls)


def svr(X, y, X_test=None, y_test=None):
    from sklearn import svm
    clf = svm.SVR()
    print clf.fit(X, y)
    if X_test and y_test:
        check(clf, X_test, y_test)
    return clf


def decision_tree(X, y, X_test=None, y_test=None):
    from sklearn import tree
    clf = tree.DecisionTreeRegressor()
    print clf.fit(X, y)
    if X_test and y_test:
        check(clf, X_test, y_test)
    return clf


def gradient_boosting(X_train, y_train, X_test=None, y_test=None):
    from sklearn.ensemble import GradientBoostingRegressor
    est = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0, loss='ls')\
        .fit(X_train, y_train)
    if X_test and y_test:
        check(est, X_test, y_test)
    return est


def neural_nlp(X_train, y_train, X_test=None, y_test=None):
    from sklearn.neural_network import MLPRegressor
    clf = MLPRegressor(hidden_layer_sizes=100).fit(X_train, y_train)
    if X_test and y_test:
        check(clf, X_test, y_test)
    return clf
