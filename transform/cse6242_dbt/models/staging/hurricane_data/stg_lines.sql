with source as (
    select * from {{ source('hurricane', 'lines') }}
),
renamed as (
    select
        ogc_fid,
        cast(stormnum as NUMERIC) as storm_num,  -- Use NUMERIC or FLOAT if needed
        stormtype as storm_type,
        cast(ss as NUMERIC) as storm_severity,  -- Use NUMERIC or FLOAT if needed
        cast(stormid as STRING) as storm_id,
        cast(year as INTEGER) as year,
        {{ convert_byte_string_to_wkt(GEOMETRY) }} AS GEOMETRY  -- Convert byte string to WKT #}
    from source
)
select * from renamed
