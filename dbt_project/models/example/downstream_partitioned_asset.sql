{{
    config(
        materialized='incremental',
    )
}}
select
        *
from {{ ref('my_initial_view') }}
{% if is_incremental() %}
WHERE date_received >= '{{ var('min_date') }}' AND date_received <= '{{ var('max_date') }}'
{% endif %}