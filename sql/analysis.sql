SELECT * FROM production_analysis LIMIT 10;

-- Query 1: Production Performance by Product
SELECT
    product_id,
    product_name,
    COUNT(batch_id) AS total_batches,
    ROUND(AVG(time_variance_min), 2) AS avg_time_variance,
    ROUND(AVG(downtime_minutes), 2) AS avg_downtime,
    ROUND(AVG(quantity_produced), 2) AS avg_quantity_produced
FROM production_analysis
GROUP BY
    product_id,
    product_name
ORDER BY avg_time_variance DESC;

-- Query 2: Production Performance by Shift
SELECT
    shift,
    COUNT(batch_id) AS total_batches,
    ROUND(AVG(time_variance_min), 2) AS avg_time_variance,
    ROUND(AVG(downtime_minutes), 2) AS avg_downtime,
    ROUND(AVG(quantity_produced), 2) AS avg_quantity_produced
FROM production_analysis
GROUP BY shift
ORDER BY avg_time_variance DESC;

-- Query 3: Production Performance by Operator
SELECT
    operator,
    COUNT(batch_id) AS total_batches,
    ROUND(AVG(time_variance_min), 2) AS avg_time_variance,
    ROUND(AVG(downtime_minutes), 2) AS avg_downtime,
    ROUND(AVG(quantity_produced), 2) AS avg_quantity_produced
FROM production_analysis
GROUP BY operator
ORDER BY avg_time_variance DESC;

-- Query 4: Downtime vs Production Performance
SELECT
    downtime_status,
    COUNT(batch_id) AS total_batches,
    ROUND(AVG(time_variance_min), 2) AS avg_time_variance,
    ROUND(AVG(downtime_minutes), 2) AS avg_downtime,
    ROUND(AVG(quantity_produced), 2) AS avg_quantity_produced
FROM production_analysis
GROUP BY downtime_status
ORDER BY avg_time_variance DESC;

-- Query 5: Top 10 Batches with Highest Downtime
SELECT
    batch_id,
    date,
    product_name,
    shift,
    actual_batch_time_min,
    standard_batch_time_min,
    time_variance_min,
    downtime_minutes,
    quantity_produced
FROM production_analysis
WHERE downtime_minutes > 0
ORDER BY downtime_minutes DESC
LIMIT 10;

-- Query 6: Downtime by Factor
SELECT
    df.factor_name,
    SUM(d.downtime_minutes) AS total_downtime
FROM downtime d
JOIN downtime_factors df
    ON d.factor_id = df.factor_id
GROUP BY df.factor_name
ORDER BY total_downtime DESC;