With get_max as (
    Select
    lines.* except(storm_type),
    max(lines.storm_severity) OVER (partition by storm_id) AS max_severity
  
  FROM {{ ref('stg_lines') }} as lines
)

Select
    storm_id,
    max_severity,
    year,
from get_max
group by all
