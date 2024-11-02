with source as (
      select * from {{ source('stock_price', 'stock_price_history') }}
),
renamed as (
    select
        date(date) as trading_date,
        _adj_close_hdx as adj_close_hd,
        _adj_close_lowx as adj_close_low,
        _adj_close_spyx as adj_close_spyx
    from source
)
select * from renamed
order by trading_date desc
  