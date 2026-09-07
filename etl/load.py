from transform import transform_data
from extract import extract_data
from sqlalchemy import create_engine

def load_data():
    production_analysis = transform_data()

    _, _, downtime, downtime_factors = extract_data()

    engine = create_engine(
        'sqlite:///manufacturing.db'
    )

    production_analysis.to_sql(
        'production_analysis',
        con=engine, if_exists ='replace',
        index=False
    )

    downtime.to_sql(
        'downtime',
        con=engine, if_exists='replace',
        index=False
    )

    downtime_factors.to_sql(
        'downtime_factors',
        con=engine, if_exists='replace',
        index=False
    )

    print('Data berhasil dimuat ke Database!')

if __name__ == '__main__':
    load_data()