import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.decomposition import PCA

def nelson_siegel(maturities: np.ndarray, beta0: float, beta1: float, beta2: float, decay: float) -> np.ndarray:
    """
    Formule analytique du modèle de structure par terme de Nelson-Siegel.
    """
    tau = maturities / decay
    factor1 = (1 - np.exp(-tau)) / (tau + 1e-8)
    factor2 = factor1 - np.exp(-tau)
    return beta0 + beta1 * factor1 + beta2 * factor2

def fit_nelson_siegel(maturities: np.ndarray, yields: np.ndarray) -> tuple:
    """
    Calibre les paramètres du modèle Nelson-Siegel par minimisation des carrés des erreurs (OLS/NLS).
    """
    def objective(params):
        b0, b1, b2, decay = params
        pred = nelson_siegel(maturities, b0, b1, b2, decay)
        return np.sum((yields - pred) ** 2)

    # Initialisation raisonnable des paramètres
    initial_guess = [yields[-1], yields[0] - yields[-1], 0.0, 1.0]
    bounds = [(-10, 20), (-20, 20), (-20, 20), (0.1, 10.0)]
    
    res = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')
    return res.x

def compute_yield_curve_pca(yield_data: pd.DataFrame, n_components: int = 3) -> tuple:
    """
    Effectue l'Analyse en Composantes Principales (PCA) sur la matrice des taux.
    Retourne les facteurs (Level, Slope, Curvature) et le ratio de variance expliquée.
    """
    clean_data = yield_data[['13W', '5Y', '10Y', '30Y']].dropna()
    pca = PCA(n_components=n_components)
    factors = pca.fit_transform(clean_data)
    
    factors_df = pd.DataFrame(factors, index=clean_data.index, columns=['Level (PC1)', 'Slope (PC2)', 'Curvature (PC3)'])
    explained_variance = pca.explained_variance_ratio_
    
    return factors_df, explained_variance