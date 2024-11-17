select 
    year,
    month,
    is_hurricane_season,
    relative_adj_close_hd,
    relative_adj_close_low,
    relative_adj_close_spyx
from {{ ref('int_gen_target') }}
where year > 2013
order by 1 desc,2 desc
