import pandas as pd

def extract_data():
    production = pd.read_csv('data/raw/production.csv')
    products = pd.read_csv('data/raw/products.csv')
    downtime = pd.read_csv('data/raw/downtime.csv')
    downtime_factors = pd.read_csv('data/raw/downtime_factors.csv')

    return production, products, downtime, downtime_factors

if __name__ == '__main__':
    production, products, downtime, downtime_factors = extract_data()

    print('Production:', production.shape)
    print('Products:', products.shape)
    print('Downtime:', downtime.shape)
    print('Downtime Factors:', downtime_factors.shape)