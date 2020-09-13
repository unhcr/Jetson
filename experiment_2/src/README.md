# Data

We rely on the following data sources:

Code | Description | Link
---|---|---|
acled | Conflict data - fatalities and incidents | acled.org


## `get_data`
Contains one module per data source, e.g. `get_acled.py`, `get_fsnau.py`.

Each module has two functions:
- `get_*_all` = retrieves all data in a range, with the option to override past downloads
- `get_*_monthy` = retrieves only the data for a specified month

NOTE: `get_ew_ea.py` has four functions, since there are two datasets: the dashboard front page, and the river levels page.

## `compile_data`

Each module has three functions:

`collect_*` = concatenates all data together
`clean_*` = cleans the data
`aggregate_*` = collapses to region and month

Each aggregated file should have two columns:
- `region`
- `month`
- and any variables (eg. `arrivals`)

Cleaned files may also have the following:

- any other nested columns (`date`, `subregion`, `previous_region`, `future_region`)