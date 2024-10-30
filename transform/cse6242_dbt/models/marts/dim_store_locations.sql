select * from {{ ref('store_locations') }}
order by state desc
