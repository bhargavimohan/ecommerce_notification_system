import click
from datetime import datetime
from models import Session, store, allowance, Notification

DATE_FORMAT = "%Y-%m"


def show_reports(input_date=None):
    try:
        if input_date:
            month = datetime.strptime(input_date, DATE_FORMAT)
            current_month = month.replace(day=1)
            allowances = (
                Session.query(allowance).filter(allowance.a_month == current_month).all()
            )
        else:
            month = datetime.today()
            allowances = Session.query(allowance).all()

        print(
            f"{'store ID':<10}{'Month':<15}{'allowance Amount':<20}{'Amount expenditure':<20}{'expenditure %':<20}"
        )
        print("-" * 75)  # Separator line

        for allowance in allowances:
            expenditure_percentage = calculate_percentage(
                expenditure=allowance.a_amount_expenditure, allowance=allowance.a_allowance_amount
            )
            click.echo(
                f"{allowance.a_store_id:<10}{str(allowance.a_month):<15}{allowance.a_allowance_amount:<20.2f}{allowance.a_amount_expenditure:<20.2f}{expenditure_percentage:<20.2f}"
            )

    except Exception as e:
        Session.rollback()  # Rollback in case of error
        print(e)  # Handle or raise the exception
    finally:
        Session.close()  # Close the session


def notify_stores(input_date=None):
    if input_date:
        month = datetime.strptime(input_date, DATE_FORMAT)
    else:
        month = datetime.today()

    current_month = month.replace(day=1)

    try:
        allowances = Session.query(allowance).filter(allowance.a_month == current_month).all()
        for allowance in allowances:
            notification = (
                Session.query(Notification)
                .filter_by(a_store_id=allowance.a_store_id, a_month=current_month)
                .first()
            )
            if not notification:
                notification = Notification(
                    a_store_id=allowance.a_store_id, a_month=current_month
                )
                Session.add(notification)

            expenditure_percentage = calculate_percentage(
                expenditure=allowance.a_amount_expenditure, allowance=allowance.a_allowance_amount
            )

            # Notify for 100% expenditure
            if (
                expenditure_percentage >= 100
                and not notification.hundred_percent_notified
            ):
                click.echo(
                    f"{month.date()} - store ID {allowance.a_store_id}: 100% of allowance reached. allowance: {allowance.a_allowance_amount}, expenditure: {allowance.a_amount_expenditure} | {expenditure_percentage:.1f}%. Setting store offline."
                )
                notification.hundred_percent_notified = True
                notification.fifty_percent_notified = True
                store = Session.query(store).filter_by(a_id=allowance.a_store_id).first()
                store.a_online = False

            # Notify for 50% expenditure only if 100% has not been reached
            elif (
                expenditure_percentage >= 50 and not notification.fifty_percent_notified
            ):
                click.echo(
                    f"{month.date()} - store ID {allowance.a_store_id}: 50% of allowance reached. allowance: {allowance.a_allowance_amount}, expenditure: {allowance.a_amount_expenditure} | {expenditure_percentage:.1f}%"
                )
                notification.fifty_percent_notified = True
        Session.commit()

        click.echo(f"Current reports as follows:")
        show_reports(input_date)

    except Exception as e:
        Session.rollback()  # Rollback in case of error
        raise e  # Handle or raise the exception
    finally:
        Session.close()  # Close the session


def modify_allowance(store_id, input_date, change):
    date = datetime.strptime(input_date, DATE_FORMAT)
    month = date.replace(day=1)

    try:
        allowance = (
            Session.query(allowance).filter_by(a_store_id=store_id, a_month=month).first()
        )
        if not allowance:
            click.echo(f"No allowance found for store ID {store_id} for the month {month}.")
            return

        original_allowance = allowance.a_allowance_amount
        allowance.a_allowance_amount = change

        # Make store online if expenditure percentage is less than 100 after a allowance change
        expenditure_percentage = calculate_percentage(
            expenditure=allowance.a_amount_expenditure, allowance=allowance.a_allowance_amount
        )
        store = Session.query(store).filter_by(a_id=allowance.a_store_id).first()
        if expenditure_percentage < 100 and not store.a_online:
            store.a_online = True
            click.echo(
                f"allowance for store ID {store_id} for the month {month} changed from {original_allowance} to {allowance.a_allowance_amount}. Setting store Online."
            )
        else:
            click.echo(
                f"allowance for store ID {store_id} for the month {month} changed from {original_allowance} to {allowance.a_allowance_amount}."
            )
        Session.commit()

        # Run Notification
        notify_stores(input_date)
    except Exception as e:
        Session.rollback()  # Rollback in case of error
        raise e  # Handle or raise the exception
    finally:
        Session.close()  # Close the session


def modify_expenditure(store_id, input_date, change):
    date = datetime.strptime(input_date, DATE_FORMAT)
    month = date.replace(day=1)
    try:
        allowance = (
            Session.query(allowance).filter_by(a_store_id=store_id, a_month=month).first()
        )
        if not allowance:
            click.echo(f"No allowance found for store ID {store_id} for the month {month}.")
            return

        original_expenditure = allowance.a_amount_expenditure
        allowance.a_amount_expenditure += change
        Session.commit()
        click.echo(
            f"expenditure amount for store ID {store_id} for the month {month} changed from {original_expenditure} to {allowance.a_amount_expenditure}."
        )
        # Run Notification
        notify_stores(input_date)
    except Exception as e:
        Session.rollback()  # Rollback in case of error
        raise e  # Handle or raise the exception
    finally:
        Session.close()  # Close the session


def calculate_percentage(expenditure, allowance):
    expenditure_percentage = (expenditure / allowance) * 100
    return expenditure_percentage
