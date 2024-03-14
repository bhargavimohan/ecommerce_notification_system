import click
from commands import notify_stores, modify_allowance, modify_expenditure, show_reports


@click.group()
def cli():
    pass


@cli.command()
@click.option("--month", required=True, type=str, help="Format: YYYY-MM")
def check_allowances(month):
    """Check allowances for the specified month."""
    notify_stores(month)


@cli.command()
@click.option("--month", default=None, type=str, help="Format: YYYY-MM")
def display_reports(month):
    """Display reports for the specified month."""
    show_reports(month)


@cli.command()
@click.option("--store-id", required=True, type=int, help="ID of the store.")
@click.option("--month", required=True, type=str, help="Format: YYYY-MM")
@click.option(
    "--change", required=True, type=float, help="Amount to adjust the allowance."
)
def adjust_allowance(store_id, month, change):
    """Adjust the allowance for a specific store and month."""
    modify_allowance(store_id, month, change)


@cli.command()
@click.option("--store-id", required=True, type=int, help="ID of the store.")
@click.option("--month", required=True, type=str, help="Format: YYYY-MM")
@click.option(
    "--change", required=True, type=float, help="Amount to adjust the amount expenditure."
)
def adjust_expenditure(store_id, month, change):
    """Adjust the amount expenditure for a specific store and month."""
    modify_expenditure(store_id, month, change)


if __name__ == "__main__":
    cli()
