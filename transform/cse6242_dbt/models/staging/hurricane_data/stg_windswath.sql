with source as (
    select * from {{ source('hurricane', 'windswath') }}
),
renamed as (
    select
        ogc_fid,
        radii,
        cast(stormid as STRING) as storm_id,
        upper(basin) as basin,
        FORMAT('%02d', cast(stormnum as int64)) as storm_num,  -- Use NUMERIC or FLOAT if needed
        PARSE_TIMESTAMP('%Y%m%d%H', CAST(startdtg AS STRING)) as hurricane_startdtg,
        PARSE_TIMESTAMP('%Y%m%d%H', CAST(enddtg AS STRING)) as hurricane_enddtg,
        cast(year as INTEGER) as hurricane_int
    from source
)
select 
    ogc_fid,
    radii,
    basin || storm_num || hurricane_int as storm_id,
    basin,
    storm_num, 
    hurricane_startdtg,
    hurricane_enddtg,
    PARSE_DATE('%Y', CAST(hurricane_int AS STRING)) as hurricane_year
from renamed
