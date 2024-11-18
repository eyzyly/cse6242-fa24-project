select * 
from {{ ref('int_add_missing_dates_stock') }}
order by 1 desc