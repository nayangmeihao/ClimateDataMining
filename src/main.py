import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def data_processed(data):
    # Check data for outliers
    import seaborn as sns
    for i in range(data.shape[1] - 9):
        sns.boxplot(x=data.iloc[:, i + 9])
        plt.show()

    # data describe
    res = pd.DataFrame(data.describe())
    res.to_csv('../data/data_describe.csv', encoding='gbk')
    # Missing value test
    print(data[data.isnull() == True].count())

    # plt.figure(figsize=(20, 20))
    # data.boxplot()
    # plt.savefig("boxplot.jpg")
    # plt.show()


def data_norm(data):
    # Z-Score
    zscore = preprocessing.StandardScaler()
    data_zs = zscore.fit_transform(data.iloc[:, 9:])
    df = pd.concat([data.iloc[:, 0], pd.DataFrame(data_zs)], axis=1)
    col_list = list(data)
    del col_list[1: 9]
    df.columns = col_list
    return df


def corr_fun(df):
    # Calculate the correlation between each variable and count
    corr_df = df.corr(method='spearman')
    outputpath = '../data/corr_result.csv'
    corr_df.to_csv(outputpath, sep=',', index=True, header=True)

    # Screening of a few variables with strong correlations for mapping
    plt.figure(figsize=(10, 8))
    sns.pairplot(data, x_vars=['Tgrassmin_Jul', 'Raindays_Dec', 'Frost_Apr'], y_vars='count', size=7, aspect=0.8,
                 kind='reg')
    plt.savefig("../img/Corr_plot.pdf")
    plt.show()


def plot_hist_fun(data):
    # Plotting histograms
    import matplotlib.pyplot as plt
    i = 14

    plt.hist(x=data.iloc[:, i],
             bins=20,
             color='steelblue',
             edgecolor='black'
             )
    plt.xlabel("value")
    plt.ylabel(data.columns[i])
    plt.savefig('../img/plot_hist.pdf')
    plt.show()


def LR_fun(df):
    X_train, X_test, Y_train, Y_test = train_test_split(df.iloc[:, 1:], df.iloc[:, 0], train_size=.80)

    model = LinearRegression()
    model.fit(X_train, Y_train)
    a = model.intercept_
    b = model.coef_  # Regression coefficient
    # print("最佳拟合线:截距", a, ",回归系数：", b)

    score = model.score(X_test, Y_test)
    print(score)
    # predict
    Y_pred = model.predict(X_test)
    print(Y_pred)

    plt.plot(range(len(Y_pred)), Y_pred, 'b', label="predict")
    plt.savefig("predict.jpg")
    plt.show()

    plt.figure()
    plt.plot(range(len(Y_pred)), Y_pred, 'b', label="predict")
    plt.plot(range(len(Y_pred)), Y_test, 'r', label="test")
    plt.legend(loc="upper right")
    plt.xlabel("test")
    plt.ylabel('test')
    plt.savefig('plot.pdf')
    plt.show()


if __name__ == '__main__':
    # imput data
    data = pd.read_csv("../data/example_climate_disease.csv")

    # Description data
    data_processed(data)  # Data pre-processing
    plot_hist_fun(data)  # Histogram for plotting features

    df = data_norm(data)  # z-score normalisation
    corr_fun(data.iloc[:, 9:])  # Calculate and plot the correlation between each variable and count
