import pandas as pd
import re
import datetime

def write_grid_search_results(gs,message, metrics, file_out='', nb_folds=2, nb_best=1, nb_models_to_edit = 10):
    """   
    Fonction qui stocke les résultats de la grid search dans un fichier Excel
    et renvoie un dataframe avec les colonnes de paramètres + les performances

    gridsearch : gridsearch object
        nom d'un objet grid search déjà exécuté
    message : str
        message pour indiquer le but de la grid search
    file_out : str, default =  ''
        (optionnel) : Chemin complet du fichier Excel à créer
        On va lui rajouter le jour+heure pour éviter d'écraser un précédent run par mégarde
    
    Credit: ==== Erwann Bargain ==== © Celtis Conseil
    """
    #On récupère les résultats dans un dataframe
    df_results = pd.DataFrame( gs.cv_results_)

    #On renomme en "valid" les occurences "test" des colonnes (pour cohérence globale)
    df_results = df_results.rename(columns=lambda x: re.sub('test','valid',x))

    #On rajoute un message expliquant la gridsearch
    df_results['message'] = message

    #on récupère le modele sans ses paramètres
    df_results['model'] = df_results['param_model'].astype(str).str.split('(').str.get(0)

    #identification de tous les paramètres du modèle pour les renommer
    dict_param_names = {}
    new_param_names = []
    for c in df_results.columns:
        if 'param_model__' in c :
            new_name = c.replace('param_model__','')
            new_param_names.append(new_name)
            dict_param_names[c]=new_name
    df_results = df_results.rename(columns= dict_param_names)

    #rajout d'un idenfifiant avant le tri
    df_results['id'] = range(1,len(df_results)+1)

    #liste pour ranger les colonnes relatives au metrics
    mean_valid_metrics = [ 'mean_valid_' + m for m in metrics]
    mean_train_metrics = [ 'mean_train_' + m for m in metrics]
    std_valid_metrics = [ 'std_valid_' + m for m in metrics]
    std_train_metrics = [ 'std_train_' + m for m in metrics]
    rank_valid_metrics_except_one = [ 'rank_valid_' + m for m in metrics[1:]]

    split_means = [ 'split' + str(i) + '_' + s + '_'  + m for i in range(nb_folds) for m in metrics for s in ['valid','train']]

    #tri des résultats : du meilleur résultat au moins bon
    df_results = df_results.sort_values('rank_valid_' + metrics[0])

    df_results = df_results[ ['message', 'rank_valid_' + metrics[0], 'model','param_standardize']
                              + new_param_names
                              + mean_valid_metrics
                              + mean_train_metrics
                              + std_valid_metrics
                              + ['mean_fit_time', 'std_fit_time', 'mean_score_time', 'std_score_time']
                              + std_train_metrics
                              + rank_valid_metrics_except_one
                              + split_means
                              + ['param_model','id']
                            ]

    ### Ecriture des résultats dans un fichier s'il y en a un d'indiqué
    if file_out != '':

        #On récupère l'heure actuelle
        hour = datetime.datetime.now().strftime("%Y-%m-%d__%H_%M_%S_")

        df_results.style.\
                        background_gradient(subset=['mean_valid_' + metrics[0]], cmap='BuGn').\
                        to_excel(file_out, engine='openpyxl'
                        , index = False
                        , freeze_panes = ((1,0))
                        , float_format="%.4f"  #on perd la valeur mais c'est bien arrondi
                        #, na_rep = '*' #default ''
                        )


    ### Partie affichage dans l'output
    df_ko = df_results[ df_results['mean_valid_' + metrics[0]].isna() ]
    if len(df_ko)>0:
        print("Modèles avec un problème lors de la grid search")
        print( df_ko[ ['id', 'model', 'param_standardize',]
                     + new_param_names ])
    else:
        print("Tous les modèles ont pu être estimés")

    print("\nMeilleurs paramètres par modèle")
    df_best = df_results.groupby('model').head(nb_best)
    print( df_best[ ['rank_valid_' + metrics[0] ] + mean_valid_metrics + ['mean_fit_time', 'model', 'param_standardize',] \
                    + new_param_names ])

    print("\n" + str(nb_models_to_edit) + " meilleurs modèles")
    print( df_results[ ['rank_valid_' + metrics[0], 'model', 'param_standardize',] \
                              + new_param_names \
                              + mean_valid_metrics + ['mean_fit_time']][:nb_models_to_edit] )


    return df_results