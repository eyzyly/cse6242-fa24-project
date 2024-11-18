WITH date_range AS (
  -- Generate a sequence of dates covering your dataset's range
  SELECT 
    day AS trading_date
  FROM 
    UNNEST(GENERATE_DATE_ARRAY(DATE('2013-11-13'), DATE('2024-11-12'))) AS day -- Adjust range as needed
),
stock_data AS (
  -- Your original stock data
  SELECT 
    trading_date,
    adj_close_hd,
    adj_close_low,
    adj_close_spyx
  FROM 
    {{ ref('base_stock_price_stock_price_history') }}
),
all_dates AS (
  -- Left join to ensure all dates are present
  SELECT
    d.trading_date,
    s.adj_close_hd,
    s.adj_close_low,
    s.adj_close_spyx
  FROM
    date_range d
  LEFT JOIN
    stock_data s
  ON
    d.trading_date = s.trading_date
),
filled_data AS (
  -- Fill missing data using LAST_VALUE
  SELECT
    trading_date,
    LAST_VALUE(adj_close_hd IGNORE NULLS) OVER (ORDER BY trading_date) AS adj_close_hd,
    LAST_VALUE(adj_close_low IGNORE NULLS) OVER (ORDER BY trading_date) AS adj_close_low,
    LAST_VALUE(adj_close_spyx IGNORE NULLS) OVER (ORDER BY trading_date) AS adj_close_spyx
  FROM
    all_dates
)
SELECT
  trading_date,
  adj_close_hd,
  adj_close_low,
  adj_close_spyx
FROM
  filled_data
ORDER BY
  trading_date
