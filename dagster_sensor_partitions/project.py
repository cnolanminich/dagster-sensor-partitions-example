from pathlib import Path

from dagster_dbt import DbtProject

dbt_project_path = Path(__file__).joinpath("..", "..", "dbt_project").resolve()

dbt_project_project = DbtProject(
    project_dir=dbt_project_path,
    packaged_project_dir=Path(__file__).joinpath("..", "dbt-project").resolve(),
)
dbt_project_project.prepare_if_dev()