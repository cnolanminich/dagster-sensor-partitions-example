from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource

from .assets import dbt_project_dbt_assets, incremental_dbt_assets
from .project import dbt_project_project, dbt_project_path
from .sensors import update_downstream_partitions_sensor
import os 
defs = Definitions(
    assets=[dbt_project_dbt_assets, incremental_dbt_assets],
    resources={
        "dbt": DbtCliResource(project_dir=dbt_project_project),
        "duckdb": DuckDBResource(database=os.path.join(os.fspath(dbt_project_path),"dev.duckdb") ),
    },
    sensors=[update_downstream_partitions_sensor],
)