select * 
from {{ ref('base_stock_price_stock_price_history') }}
order by 1 desc