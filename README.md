# dagster-sensor-partitions-example
 

## Introduction

This demo project explores how you might have serve the following use case:

* Have a Dagster asset to manage an asset that you only refresh when there is a logical change, but where the data could still be flowing (e.g., a dbt model view, or a Snowflake dynamic table)
* Have downstream partitioned Dagster assets that you want to run
* Have late arriving facts in your upstream Dagster assets, so you want a way to trigger partitions in the downstream based on a query and _not_ based on a partition metadata

## Implementation

In this project, we have a dbt project with `my_initial_view` (which for this purpose is a table where you manually make changes to it, but you can see how it would work with a view with underlying data changes), a `downstream_partitioned_asset` incremental dbt model, is partitioned daily.

When `my_initial_view` gets different data, a sensor (`update_downstream_partitions_sensor`) will pick up the difference and compute hashes for the dates in question and compares them to the previous dates and hashes of values.


## Some Caveats about this setup

* If you update _all_ of the source updates, it will trigger a large backfill
* Using duckdb locally with a `dagster dev` deployment, you will get concurrent write errors. On a production instance of Dagster, you can set concurrency limits, and of course production data warehouses can handle concurrent workloads as well.
* The sensor function that polls the table could be expensive as the number of dates grows. This could be addressed by setting a ceiling (e.g., only look back for the most recent 100 days)


## Steps to Implement

* run `dagster dev`
* turn on the sensor
* materialize `my_initial_view`
* if you want to see the logic work, comment out the first block and uncomment the second in `my_intial_view`, materialize `my_initial_view` to get the new data in, and the sensor will pick up changes