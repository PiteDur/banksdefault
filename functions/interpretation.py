import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns   

def permutation_importance(model, model_score, data, labels, col_var, N, type_score="f1", variable=False, save=False):
    """
    model: classification model that has been estimated and that allows prediction (class model)
    model_score: score given by the model (float or integer)
    data: data on which the score has been calculated (numpy array or pandas dataframe)
    labels: labels corresponding to data (np array or pandas dataframe)
    col_var: list of the column 
    N: integer, number of time we want to schufle the column
    type_score: string refering to the type of score to be calculated during the permutation importance. Must be the same as "model_score".
    variable: name of a variable to be plotted in red in the final histogram
    save: False or string variable with the path for saving the plot
    """

    dic_scores = {}

    sns.set_style("darkgrid")

    # SHUFFLED SCORES CALCULATION
    for k, var_k in enumerate(col_var):
        dic_scores[var_k] = []

        for n in range(N + 1):
            df_temp = data.copy()
            df_temp[var_k] = np.random.permutation(df_temp[var_k])

            y_predict_temp = model.predict(df_temp)

            cross_tab_temp = pd.crosstab(labels, y_predict_temp).values
            a, b, c, d = cross_tab_temp[0, 0], cross_tab_temp[0, 1], cross_tab_temp[1, 0], cross_tab_temp[1, 1]

            precision = d / (d + b)
            recall = d / (d + c)
            f1 = 2 * (precision * recall) / (precision + recall)

            if type_score == "f1":
                dic_scores[var_k].append(f1)
            elif type_score == "precision":
                dic_scores[var_k].append(precision)
            else:
                dic_scores[var_k].append(recall)

    # MEAN SHUFFLED SCORE BY VARIABLE
    l_importance = [[model_score - np.mean(dic_scores[var]), var] for var in col_var]

    # ORDERING SCORES
    l_importance = sorted(l_importance)

    l_NameFeatImp, l_FeatImp = [importance[1] for importance in l_importance], [float(importance[0]) for importance in l_importance]

    fig, ax = plt.subplots(figsize=(18, 10))
    ax.barh(l_NameFeatImp, l_FeatImp, alpha=0.8)

    ax.tick_params(axis='y', labelsize=13)
    ax.tick_params(axis='x', labelsize=15)

    if variable and variable in l_NameFeatImp:
        a = l_NameFeatImp.index(variable)
        ax.get_children()[a].set_color('r')

    if save:
        plt.savefig(save)

    plt.show()

    return l_importance