import unittest
from datetime import date
from sqlalchemy import create_engine
from models import Base, store, allowance, Notification, Session
from commands import notify_stores

TEST_DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/test_store_allowances"

engine = create_engine(TEST_DATABASE_URL)
Session.configure(bind=engine)


class TestEcommerceApp(unittest.TestCase):
    @classmethod
    def setUpClass(
        cls,
    ):
        # run once before any tests in the class are run - to set up test data
        # Create all the tables defined in your models
        Base.metadata.create_all(engine)

        # Populate mock data for stores
        stores_data = [(1, "Teststore1", 1), (2, "Teststore2", 0), (3, "Teststore3", 1)]
        for s_id, s_name, s_online in stores_data:
            store = store(a_id=s_id, a_name=s_name, a_online=s_online)
            Session.add(store)

        Session.commit()

        # Populate mock data for allowances
        allowances_data = [
            (1, "2020-06-01", 100.00, 50.00),  # 50% expenditure
            (2, "2020-06-01", 100.00, 100.00),  # 100% expenditure
            (3, "2020-06-01", 100.00, 120.00),  # > 100% expenditure
        ]
        for b_store_id, b_month, b_allowance, b_expenditure in allowances_data:
            allowance = allowance(
                a_store_id=b_store_id,
                a_month=b_month,
                a_allowance_amount=b_allowance,
                a_amount_expenditure=b_expenditure,
            )
            Session.add(allowance)

        Session.commit()
        Session.close()

    @classmethod
    def tearDownClass(cls):
        # run once after all tests in the class have been run - to clean up
        Base.metadata.drop_all(engine)

    def test_check_allowances(self):
        notify_stores(input_date="2020-06")

    def test_fifty_percent_notification(self):
        notify_stores(input_date="2020-06")
        notified_store = Session.query(Notification).filter_by(a_store_id=1).one_or_none()
        self.assertIsNotNone(notified_store)
        self.assertTrue(notified_store.fifty_percent_notified)
        self.assertFalse(notified_store.hundred_percent_notified)
        Session.close()

    def test_hundred_percent_notification_and_offline(self):
        notify_stores(input_date="2020-06")
        notified_store = Session.query(Notification).filter_by(a_store_id=2).one_or_none()
        store_status = Session.query(store).filter_by(a_id=3).one()
        self.assertIsNotNone(notified_store)
        self.assertTrue(notified_store.hundred_percent_notified)
        self.assertFalse(store_status.a_online)
        Session.close()

    def test_no_double_fifty_percent_notification(self):
        # Ensure no multiple notification
        notify_stores(input_date="2020-06")  # run once
        notify_stores(input_date="2020-06")  # run twice
        notified_store = Session.query(Notification).filter_by(a_store_id=1).one_or_none()
        self.assertIsNotNone(notified_store)
        self.assertTrue(notified_store.fifty_percent_notified)
        self.assertFalse(notified_store.hundred_percent_notified)
        Session.close()

    def test_no_double_hundred_percent_notification_and_offline(self):
        # Ensure no multiple notification
        notify_stores(input_date="2020-06")  # run once
        notify_stores(input_date="2020-06")  # run twice
        notified_store = Session.query(Notification).filter_by(a_store_id=2).one_or_none()
        store_status = Session.query(store).filter_by(a_id=3).one()
        self.assertIsNotNone(notified_store)
        self.assertTrue(notified_store.hundred_percent_notified)
        self.assertFalse(store_status.a_online)
        Session.close()


if __name__ == "__main__":
    unittest.main()
