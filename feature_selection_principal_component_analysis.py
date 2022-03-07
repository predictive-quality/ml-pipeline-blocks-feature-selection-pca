# Copyright (c) 2022 RWTH Aachen - Werkzeugmaschinenlabor (WZL)
# Contact: Simon Cramer, s.cramer@wzl-mq.rwth-aachen.de

from sklearn.decomposition import PCA
import pandas as pd
from absl import logging
from s3_smart_open import get_filenames, read_pd_fth, to_pd_fth, to_pckl, read_pckl

def pca(x, total_variance, pca):
    """Principal Component Analysis: 
        The amount of variables can be reduced while maximizing the obtained variance. This entails a rotation 
        of the coordinate system in order to point to the directions of maximal variance.

    Args:
        x (class): pandas.DataFrame: features for pca scaling 
        total_variance (float): sum of highest variances of all individual principal components
        pca (class): sklearn.decomposition.PCA for pca scaling

    Returns:
        [class]: pandas.DataFrame  containing results of pca: samples as rows and principal components as columns 
    """    

    if not pca:
        pca = PCA()   
        res = pca.fit_transform(x)
        if total_variance == 1:
            i = x.shape[1]
            variance = 1.0
        else:
            variance = 0.0
            i = 0
            while variance < total_variance and i < x.shape[1]:  
                logging.debug('Percentage of variance explained by each of the selected components {}'.format(pca.explained_variance_ratio_[i]))
                variance += pca.explained_variance_ratio_[i]
                logging.info('pca_explaiend: \n {}'.format(pca.explained_variance_ratio_[i]))
                i += 1
        pca.components_ = pca.components_[0:i ,:]
    else:
        res = pca.transform(x)
        i = pca.components_.shape[0]
        variance = sum(pca.explained_variance_ratio_[0:i])

    res_evr = res[:, 0:i] 
    colnames = ['pc_'+str(i) for i in range(res_evr.shape[1])]
    df_res_evr = pd.DataFrame(res_evr, columns=colnames)

    logging.info('Have {} features (input) reduced to {} and sustained {:.8} % of variance.'.format(x.shape[1], df_res_evr.shape[1], variance*100))

    return df_res_evr, pca 


def inverse_pca(x, pca):
    """Inverse scale a pandas.DataFrame with principal components to the original data.

    Args:
        x (class): pandas.DataFrame: principal components for inverse pca scaling
        pca (class): sklearn.decomposition.PCA for pca inverse scaling (inverse_transform)

    Returns:
        [class]: pandas.DataFrame with the reconstructed data
    """
    x_original = pca.inverse_transform(x)
    colnames = ['feature_'+str(i) for i in range(x_original.shape[1])]
    df_x = pd.DataFrame(x_original, columns=colnames)
    logging.info('Inverse scaled pca features from shape {} to shape {}'.format(x.shape,x_original.shape))

    return df_x, pca
