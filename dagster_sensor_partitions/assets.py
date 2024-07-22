from dagster import AssetExecutionContext, DailyPartitionsDefinition, OpExecutionContext, BackfillPolicy
from dagster_dbt import DbtCliResource, dbt_assets

from .project import dbt_project_project
import json

daily_partitions = DailyPartitionsDefinition(start_date="2023-05-25")


@dbt_assets(manifest=dbt_project_project.manifest_path,
            select = "my_initial_view")
def dbt_project_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    


@dbt_assets(
    manifest=dbt_project_project.manifest_path,
    project=dbt_project_project,
    select="downstream_partitioned_asset",
    partitions_def=daily_partitions,
    backfill_policy=BackfillPolicy.single_run(),
)
def incremental_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
     # map partition key range to dbt vars
    first_partition, last_partition = context.asset_partitions_time_window_for_output(
        list(context.selected_output_names)[0]
    )
    dbt_vars = {"min_date": str(first_partition), "max_date": str(last_partition)}
    dbt_args = ["build", "--vars", json.dumps(dbt_vars)]

    # Invoke dbt CLI
    dbt_cli_task = dbt.cli(dbt_args, context=context)

    # Emits an AssetObservation for each asset materialization, which is used to
    # identify the Snowflake credit consumption
    yield from dbt_cli_task.stream()

    # # fetch run_results.json to log compiled SQL
    # run_results_json = dbt_cli_task.get_artifact("run_results.json")
    # for result in run_results_json["results"]:
    #     model_name = result.get("unique_id")
    #     context.log.info(f"Compiled SQL for {model_name}:\n{result['compiled_code']}")

