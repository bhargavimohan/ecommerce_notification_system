# store allowance Management CLI

## Introduction

This command-line tool helps manage and notify stores about their monthly allowances and expenditures. The tool is built using Python and the `click` library. It can notify stores when they hit 50% or 100% of their allowances and also allows allowance or amount expenditure modifications for a specific store for a given month.

## Requirements

- Python 3.x
- MySQL 8.0.35
- Required Python packages: `click`, `sqlalchemy`

## Setup

1. Create a database in MySQL named `ecommercestore`.
2. Run `migration.sql`(presuming after `db.sql`) to initialize the database schema and sample data.
3. Ensure the `commands.py`, `models.py`, and the main CLI script are in the same directory.
4. Update the database connection details in `models.py` if required.

## CLI Usage

### 1. Check allowances:

Checks and notifies stores if they have reached 50% or 100% of their monthly allowances.

Command:

python main_script.py check_allowances --month YYYY-MM

Example:

python main_script.py check_allowances --month 2020-06


### 2. Display reports:

Displays the allowance statistics for the given month.

Command:

python main_script.py display_reports --month YYYY-MM

Example:

python main_script.py display_reports --month 2020-07


### 3. Adjust allowance:

Modifies the allowance for a specific store for a given month.

Command:

python main_script.py adjust_allowance --store-id <store_id> --month YYYY-MM --change <amount>

Example:

python main_script.py adjust_allowance --store-id 1 --month 2020-06 --change 100


### 4. Adjust amount expenditure:

Modifies the amount expenditure for a specific store for a given month.

Command:

python main_script.py adjust_expenditure --store-id <store_id> --month YYYY-MM --change <amount>

Example:

python main_script.py adjust_expenditure --store-id 2 --month 2020-07 --change -50


## Edge Cases and Explanations

- *Missing Date*: If the date is not provided to `check_allowances` or `display_reports`, it will default to the current month.

- *Non-Existing store*: If adjusting the allowance or amount expenditure for a store ID that does not exist, the CLI will inform that no allowance was found for that store ID for the given month.

- *Notifications*: If the amount expenditure is more than 50% and either less than 100% or more than 100%, then the 50% notification flag is assumed to be `True`. Furthermore, The system will notify when 50% or 100% of the allowance is reached. If the allowance is already over 100% and it's changed to bring it below 100%, the system will re-notify the allowance and expenditure changes according to the notification rules(50% or 100% flags and notifying stores). The system also displays the current reports of all stores for the given month. 

## Testing

1. Create a separate test database in MySQL named `test_store_allowances`.
2. Run `migration.sql` to initialize the database schema in the test environment.
3. Update test configuration to point to this test database.
4. Mock data similar to the provided `db.sql` data is used to ensure accurate testing.
5. The testing mechanism includes setting up the database with mock data, running tests, and then tearing down to clear the test database.

## Future Enhancements

1. Implement Dockerization to improve standardization and scalability. Initial Docker-related files can be found in the `ecommerce_app` directory.
- `Dockerfile`: Defines the steps to build a Docker image for the application.
- `docker-compose.yml`: Specifies the services and configurations of mysql and python for multi-container deployment.


## Conclusion

This CLI tool provides a straightforward way to manage store allowances and notify them of their spending status.