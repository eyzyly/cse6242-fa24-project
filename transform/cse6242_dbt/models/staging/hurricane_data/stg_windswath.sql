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
        cast(year as INTEGER) as hurricane_year
    from source
)
select 
    ogc_fid,
    radii,
    basin || storm_num || hurricane_year as storm_id,
    basin,
    storm_num, 
    hurricane_startdtg,
    hurricane_enddtg,
    hurricane_year
from renamed
