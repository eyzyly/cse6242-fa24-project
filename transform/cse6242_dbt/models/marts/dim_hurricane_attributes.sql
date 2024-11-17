select * from {{ ref('int_join_max_hurricane_severity_windswath') }}
where max_severity is not null
order by hurricane_year desc
