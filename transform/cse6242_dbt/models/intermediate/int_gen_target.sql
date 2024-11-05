WITH MonthlyAverages AS (
  SELECT
    DATE_TRUNC(trading_date, MONTH) AS month,
    EXTRACT(YEAR FROM trading_date) AS year,
    CASE
      WHEN EXTRACT(MONTH FROM trading_date) BETWEEN 6 AND 11 
      THEN 1
      ELSE 0
    END AS is_hurricane_season,
    AVG(adj_close_hd) AS avg_adj_close_hd,
    AVG(adj_close_low) AS avg_adj_close_low,
    AVG(adj_close_spyx) AS avg_adj_close_spyx,
  FROM {{ ref('base_stock_price_stock_price_history') }}
  group by 1,2,3
),
NonHurricaneAverages AS (
  SELECT
    year,
    AVG(avg_adj_close_hd) AS non_hurricane_avg_hd,
    AVG(avg_adj_close_low) AS non_hurricane_avg_low,
    AVG(avg_adj_close_spyx) AS non_hurricane_avg_spyx
  FROM MonthlyAverages
  WHERE is_hurricane_season = 0
  GROUP BY year
)
SELECT
  m.year,
  m.month,
  m.is_hurricane_season,
  m.avg_adj_close_hd / nh.non_hurricane_avg_hd AS relative_adj_close_hd,
  m.avg_adj_close_low / nh.non_hurricane_avg_low AS relative_adj_close_low,
  m.avg_adj_close_spyx / nh.non_hurricane_avg_spyx AS relative_adj_close_spyx
FROM MonthlyAverages m
JOIN NonHurricaneAverages nh ON m.year = nh.year
