from setuptools import find_packages, setup

setup(
    name="dagster_sensor_partitions",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "dagster_sensor_partitions": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dagster-duckdb",
        "dbt-duckdb<1.9",
        "pandas",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)