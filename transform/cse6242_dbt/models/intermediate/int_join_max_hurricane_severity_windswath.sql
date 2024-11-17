With windswath as (
    Select 
        ogc_fid,
        storm_id,
        basin,
        hurricane_startdtg,
        hurricane_enddtg,
        hurricane_year,
        ROW_NUMBER() OVER (PARTITION BY storm_id ORDER BY ogc_fid) AS row_num
    FROM {{ ref('stg_windswath') }} as windswath
),

filter_on_1st_row as (
    SELECT 
    ogc_fid,
    storm_id,
    basin,
    hurricane_startdtg,
    hurricane_enddtg,
    hurricane_year
FROM windswath
WHERE row_num = 1
group by all
),

lines as (
    Select
        storm_id,
        max_severity
    FROM {{ ref('int_max_hurricane_severity') }} as lines
    group by all
)

Select
    windswath.storm_id,
    lines.max_severity,
    windswath.basin,
    windswath.hurricane_startdtg,
    windswath.hurricane_enddtg,
    windswath.hurricane_year
FROM filter_on_1st_row as windswath
FULL OUTER JOIN lines
ON lines.storm_id = windswath.storm_id

group by all
