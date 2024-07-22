
-- /* first version of the view */
-- select 1 as initial_value, current_date - 1 as date_received,
-- union all
-- select 2 as initial_value, current_date - 1 as date_received,
-- union all  
-- select 3 as initial_value, current_date - 1 as date_received,
-- union all
-- select 4 as initial_value, current_date - 2 as date_received,
-- union all
-- select 5 as initial_value, current_date - 2 as date_received,
-- union all  
-- select 6 as initial_value, current_date - 2 as date_received,
-- union all
-- select 7 as initial_value, current_date - 3 as date_received,
-- union all
-- select 8 as initial_value, current_date - 3 as date_received,
-- union all  
-- select 9 as initial_value, current_date - 3 as date_received

/* second version of the view -- current_date - 1 and -2 have a change, -3 is the same */
select -1 as initial_value, current_date - 1 as date_received,
union all
select 2 as initial_value, current_date - 1 as date_received,
union all  
select 3 as initial_value, current_date - 1 as date_received,
union all
select 4 as initial_value, current_date - 2 as date_received,
union all
select -5 as initial_value, current_date - 2 as date_received,
union all  
select 6 as initial_value, current_date - 2 as date_received,
union all
select 7 as initial_value, current_date - 3 as date_received,
union all
select 8 as initial_value, current_date - 3 as date_received,
union all  
select 9 as initial_value, current_date - 3 as date_received

/* */
/* third version of the view -- current_date - 1 and -3 have a change, -2 is the same */
-- select -1 as initial_value, current_date - 1 as date_received,
-- union all
-- select -2 as initial_value, current_date - 1 as date_received,
-- union all  
-- select 3 as initial_value, current_date - 1 as date_received,
-- union all
-- select 4 as initial_value, current_date - 2 as date_received,
-- union all
-- select -5 as initial_value, current_date - 2 as date_received,
-- union all  
-- select 6 as initial_value, current_date - 2 as date_received,
-- union all
-- select 7 as initial_value, current_date - 3 as date_received,
-- union all
-- select -8 as initial_value, current_date - 3 as date_received,
-- union all  
-- select 9 as initial_value, current_date - 3 as date_received
