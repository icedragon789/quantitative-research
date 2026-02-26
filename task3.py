
# SOURCE: https://www.geeksforgeeks.org/machine-learning/building-your-first-machine-learning-model/

import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression

import warnings

MODEL_NUM = 1 # 0: Logistic Regression, 1: XGBoost, 2: SVM

def insights(df : pd.DataFrame):
    # Get insights about the data
    # df.head()
    # df.info()
    # df.describe().T
    # df.isnull().sum() # NO NULLS!
    # df.hist(bins=20, figsize=(10, 10))
    # plt.show()
    # See the correlation between each column
    # res = df.corr()
    # print(res)

    
    # Note: Keep credit_lines_outstanding as it is a more direct measure of the number of loans a borrower has, 
    # which can be an important factor in assessing credit risk. Total_debt_outstanding and loan_amt_outstanding 
    # may be correlated with credit_lines_outstanding, but they do not provide additional information about the 
    # number of loans a borrower has, which is a key factor in determining their creditworthiness.

    # Compute correlation matrix
    co_mtx = df.corr(numeric_only=True)

    # Print correlation matrix
    print(co_mtx)

    # Plot correlation heatmap
    sb.heatmap(co_mtx, cmap="YlGnBu", annot=True)

    # Display heatmap
    plt.show()

def performance(ytest, models, xtest):
    # Evaluate the models' performance
    cm = confusion_matrix(ytest, models[1].predict(xtest))

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=models[1].classes_)
    disp.plot()

    print(metrics.classification_report(ytest,
                                    models[1].predict(xtest)))

if __name__ == "__main__": 
    warnings.filterwarnings("ignore")
    
    df = pd.read_csv("Task 3 and 4_Loan_Data.csv" )
    df = df.drop(columns=['total_debt_outstanding', 'loan_amt_outstanding', 'customer_id'])

    # Insights here
    # insights(df)
    # ---------------------------------------------

    features = df.drop(['default'], axis=1)
    target = df['default']

    # Drop redundant features that will negatively effect the model's performance

    xtrain, xtest, ytrain, ytest = train_test_split(
        features, target, test_size=0.2, random_state=40)

    xtrain.shape, xtest.shape

    # Normalize the data
    norm = MinMaxScaler()
    xtrain = norm.fit_transform(xtrain)
    xtest = norm.transform(xtest)

    # Data has been prepared, let's train the model.
    models = [LogisticRegression(), XGBClassifier(), SVC(kernel='rbf', probability=True)]

    for i in range(3):
        models[i].fit(xtrain, ytrain)

        # print(f'{models[i]} : ')
        # print('Training Accuracy : ', metrics.roc_auc_score(ytrain, models[i].predict(xtrain)))
        # print('Validation Accuracy : ', metrics.roc_auc_score(
        #     ytest, models[i].predict(xtest)))
        # print()

    # Eval here
    #performance(ytest, models, xtest)
    # Accessing arguments
    script_name = sys.argv[0]

    # Example inputs
    # credit_lines_outstanding, income, years_employed, fico_score
    # NO DEFAULT: 0, 78039.38546, 5, 605
    # DEFAULT: 	5, 7442532, 1, 572
    input_prediction = [[]]
    if len(sys.argv) > 4:
        credit_lines_outstanding = int(sys.argv[1])
        income = float(sys.argv[2])
        years_employed = int(sys.argv[3])
        fico_score = int(sys.argv[4])
        input_prediction = [[credit_lines_outstanding, income, years_employed, fico_score]]

    else:
        input_prediction = [[0, 76750.28031, 8, 6606]]
        print("Using default input for prediction: " + str(input_prediction))

    predictions = models[1].predict(input_prediction)
    class_probabilities = models[1].predict_proba(input_prediction)

    default = bool(predictions[0])
    if default == True:
        print("Probability of Defaulting: " + str(class_probabilities[0][1]*100) + "%")
    else:
        print("Probability of NOT Defaulting: " + str(class_probabilities[0][0]*100) + "%")

