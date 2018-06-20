# Fast and stable database connector for Splunk
Goal is to create a replacement for Splunk DB Connect v3, which is slow and buggy in places. In order to accomplish this, we take advantage of a native agent program, [DataSnake Core](https://github.com/sodle/DataSnake-Core), written in Python. The TA communicates with the agent process in a predictable way through standard IO, allowing for potential drop-in replacements to be written created by other developers in other languages.

## Alpha
DataSnake is currently in an alpha state. Known issues:
 * If DataSnake is installed alongside Splunk DB Connect, DB Connect's user interface breaks.
 * If the DataSnake Core is installed on Python 3 instead of Python 2, an error about the missing `setdefaultencoding` function is logged. This error appears to be harmless.
 * GUI for configuring connections, inputs, etc. is absent.
 * Timestamp columns are sometimes handled in odd ways (converted to epoch format or replaced with `NaT`).
 * If you delete a tailing input, then create a new one with the same name, the old checkpoint remains. This can cause historical data from the new input to not be ingested.
 * Checkpoints are stored in `search/local/passwords.conf` instead of `TA-DataSnake/local/passwords.conf`.
 
## Supported Databases
TA-DataSnake supports all databases supported by Python's SQLAlchemy framework, including:
 * Postgres
 * SQLite
 * MySQL
 * Oracle
 * Microsoft SQL Server
 
Drivers for these must be installed alongside the DataSnake Core. See SQLAlchemy's [documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html) for a list of supported drivers and help formatting your connection string.

## Installing the Core
TA-DataSnake requires the [DataSnake Core](https://github.com/sodle/DataSnake-Core) to be installed on the system Python interpreter. This allows the use of advanced Python packages like Pandas, SQLAlchemy, and various database drivers to be used despite the limitations of Splunk's built-in interpreter.

```bash
pip install datasnake
```

This package should be installed globally and on Python 2.7.

To verify the install and check the versions of DataSnake, Python, and certain DB connectors, run:
```bash
datasnake --env
```

## Installing the TA
To build a Splunk package from this repo, run
```bash
pip install requirements-dev.txt
./build.py
```

This creates `TA-DataSnake.tar.gz` in this directory, which can be installed as a Splunk app.

## Creating a connection
DataSnake uses the Splunk secure password store to manage database connections. To add your own connections, create a new stanza in `TA-DataSnake/local/passwords.conf`:
```
[credential:TA-DataSnake-Connection:<name for the connection>:]
password = <SQLAlchemy connection string>
```

## Running a database query using the Ouroboros custom search command
```
| ouroboros connection=<connection name> query="<SQL query>"
```

## Ingest all results of a query
Add a stanza to `TA-DataSnake/local/inputs.conf`:
```
[datasnake_read://<name for the input>]
connection = <connection name>
query = <SQL query>
format = <format in which to ingest rows - "json" or "dbx">
interval = <how often in seconds to reread the database (omit to only ingest once)
```

## Tail a database table, indexing only new rows based on a rising timestamp column
Add a stanza to `TA-DataSnake/local/inputs.conf`:
```
[datasnake_tail://<name for the input>]
connection = <connection name>
query = <SQL query>
timestamp_column = <name of the column containing the rising timestamp>
format = <format in which to ingest rows - "json" or "dbx">
interval = <how often in seconds to check for new rows (omit to only ingest once)
```
