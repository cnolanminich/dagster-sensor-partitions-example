from dagster import (
    sensor,
    RunRequest,
    SensorEvaluationContext,
    SkipReason,
)
from dagster_duckdb import DuckDBResource
import json
import pandas as pd


@sensor(asset_selection=['downstream_partitioned_asset'])
def update_downstream_partitions_sensor(context: SensorEvaluationContext, duckdb: DuckDBResource):
    # Execute the query to get the current state
    query = """
    SELECT
        date_received,
        MD5(CAST(SUM(initial_value) AS VARCHAR)) AS hashed_result
    FROM
        dev.main.my_initial_view
    GROUP BY
        date_received
     """
    with duckdb.get_connection() as conn:
        current_state = pd.read_sql(query, conn, dtype={'date_received': str})
        context.log.info(f"Current state: {current_state}")
        context.log.info(f"Column types: {current_state.dtypes}")
    
    # Parse the current state into a dictionary
    current_state_dict = current_state.set_index('date_received')['hashed_result'].to_dict()
    context.log.info(f"Current state dict: {current_state_dict}")
    # Get the previous state from the cursor
    previous_state = json.loads(context.cursor) if context.cursor else {}

    # Determine which dates have changed
    changed_dates = {
        date: hash_agg for date, hash_agg in current_state_dict.items()
        if date not in previous_state or previous_state[date] != hash_agg
    }
    context.log.info(f"Changed dates: {changed_dates.keys()}")

    if not changed_dates:
        return SkipReason("No new updates found in the table.")

    context.update_cursor(json.dumps(current_state_dict))
    # Trigger downstream partitions for the changed dates
    run_requests = [
        RunRequest(run_key=f"run_for_{date}_{hash_agg}", partition_key=date)
        for date, hash_agg in changed_dates.items()
    ]
    return run_requests