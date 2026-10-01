import pandas as pd
import yfinance as yf

# Tickers des taux du Trésor US
TREASURY_TICKERS = {
    '^IRX': '13W',
    '^FVX': '5Y',
    '^TNX': '10Y',
    '^TYX': '30Y'
}

def fetch_yield_curve_data(start_date: str = '2015-01-01') -> pd.DataFrame:
    """
    Récupère les taux d'intérêt souverains et construit la matrice de la courbe des taux.
    """
    data = yf.download(list(TREASURY_TICKERS.keys()), start=start_date, progress=False)['Close']
    data = data.rename(columns=TREASURY_TICKERS)
    
    # Nettoyage et interpolation linéaire des valeurs manquantes
    data = data[['13W', '5Y', '10Y', '30Y']].dropna(how='all').ffill()
    
    # Calcul du Spread 10Y-13W (Indicateur clé de récession)
    data['Spread_10Y_13W'] = data['10Y'] - data['13W']
    
    return data