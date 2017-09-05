from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy

def run_experiemnt(all_data):
    numpy.random.shuffle(all_data)
    training_data, test_data = train_test_split(all_data, test_size=0.2)

    train_features = []
    train_results = []
    for line in training_data:
        train_features.append(line[0:6])
        train_results.append(line[6])

    reg = linear_model.LinearRegression()
    reg.fit(train_features, train_results)

    test_features = []
    test_results = []
    for line in test_data:
        test_features.append(line[0:6])
        test_results.append(line[6])

    test_predictions = reg.predict(test_features)

    print(reg.coef_ , '\t', reg.intercept_, '\t', mean_squared_error(test_results, test_predictions), '\t', r2_score(test_results, test_predictions))
    return reg.coef_, reg.intercept_, mean_squared_error(test_results, test_predictions), r2_score(test_results, test_predictions)

    #print("Coefs:", reg.coef_)
    #print("Intercept:", reg.intercept_)
    #print("MSE:", )
    #print("R^2:",)

with open('../data/percent_added_statements.txt', 'rb') as f:
    all_data = pickle.load(f)
    num_runs = 50

    intercept = mse = r2 = 0
    experiment_results = []

    for i in range(num_runs):
        results = run_experiemnt(all_data)
        experiment_results.append(results)
        intercept += results[1]
        mse += results[2]
        r2 += results[3]

    intercept /= num_runs
    mse /= num_runs
    r2 /= num_runs

    print("Final tally:\nIntercept:", intercept, "\nMSE:", mse, "\nR^2", r2)

    intercepts = pd.DataFrame([res[1] for res in experiment_results])
    intercepts.plot(kind='density')
    plt.show()

    mses = pd.DataFrame([res[2] for res in experiment_results])
    mses.plot(kind='density')
    plt.show()

    r2s = pd.DataFrame([res[3] for res in experiment_results])
    r2s.plot(kind='density')
    plt.show()