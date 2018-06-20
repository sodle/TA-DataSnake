[datasnake_read://<name>]
* Index the results of a database query in their entirety.

* Connection name as defined in DataSnake setup
connection = <value>

* SQL Query
query = <value>

* Format of rows (JSON or classic DBX)
format = [json|dbx]


[datasnake_tail://<name>]
* Follow the results of a database query by a rising timestamp column.

* Connection name as defined in DataSnake setup
connection = <value>

* SQL Query
query = <value>

* Column name used for populating event timestamp and checkpoints
timestamp_column = <value>

* Format of rows (JSON or classic DBX)
format = [json|dbx]