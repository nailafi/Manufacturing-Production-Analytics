from extract import extract_data

def transform_data():
    production, products, downtime, downtime_factors = extract_data()

    production_analysis = production.merge(
        products, on='product_id',
        how='left'
    )

    production_analysis['time_variance_min'] = (
        production_analysis['actual_batch_time_min'] - 
        production_analysis['standard_batch_time_min']
    )

    downtime_per_batch = (
        downtime.groupby('batch_id')['downtime_minutes']
        .sum().reset_index()
    )

    production_analysis = production_analysis.merge(
        downtime_per_batch, on='batch_id',
        how='left'
    )

    production_analysis['downtime_minutes'] = (
        production_analysis['downtime_minutes'].fillna(0)
    )

    production_analysis['downtime_status'] = production_analysis[
        'downtime_minutes'
    ].apply(
        lambda x: 'Has Downtime' if x > 0 else 'No Downtime'
    )

    return production_analysis

if __name__ == '__main__':
    production_analysis = transform_data()

    print(production_analysis[
        ['batch_id', 'product_id', 'actual_batch_time_min',
         'standard_batch_time_min', 'time_variance_min',
         'downtime_minutes', 'downtime_status']
    ].head())

    print("\nShape:", production_analysis.shape)