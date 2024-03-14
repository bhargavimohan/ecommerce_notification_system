CREATE TABLE t_stores (
    a_id        INT(11)         NOT NULL AUTO_INCREMENT,
    a_name      VARCHAR(255)    NOT NULL,
    a_online    BOOLEAN         NOT NULL,
    PRIMARY KEY (a_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        
CREATE TABLE t_allowances (
    a_store_id       INT(11)         NOT NULL REFERENCES t_stores (a_id),
    a_month         DATE            NOT NULL,
    a_allowance_amount DECIMAL(10,2)   NOT NULL,
    a_amount_expenditure  DECIMAL(10,2)   NOT NULL,
    PRIMARY KEY (a_store_id, a_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO t_stores
    (a_id,  a_name,             a_online)
VALUES
    (1,     'Reliance',    1),
    (2,     'Lifestyle',   0),
    (3,     'Shoppers stop',  1),
    (4,     'Pantaloons',              0),
    (5,     'Home Decor',        1),
    (6,     'Brand factory',   0),
    (7,     'Big bazaar',     1),
    (8,     'Max',    1);

INSERT INTO t_allowances
    (a_store_id, a_month, a_allowance_amount, a_amount_expenditure)
VALUES
    (1, '2023-05-01', 1030.00, 525.68),
    (2, '2023-05-01', 1990.00, 986.60),
    (3, '2023-05-01', 850.00, 655.88),
    (4, '2023-05-01', 2140.00, 753.09),
    (5, '2023-05-01', 1830.00, 942.80),
    (6, '2023-05-01', 840.00, 444.00),
    (7, '2023-05-01', 580.00, 200.71),
    (8, '2023-05-01', 490.00, 320.30),
    (1, '2023-10-01', 3160.00, 1004.81),
    (2, '2023-10-01', 4470.00, 2371.61),
    (3, '2023-10-01', 1090.00, 100.31),
    (4, '2023-10-01', 2690.00, 1999.20),
    (5, '2023-10-01', 970.00, 500.84),
    (6, '2023-10-01', 7700.00, 5040.99),
    (7, '2023-10-01', 290.00, 99.00),
    (8, '2023-10-01', 710.00, 555.00);


-- To be run after db.sql
-- Create t_notifications table for e-commerce store
CREATE TABLE t_notifications (
    a_store_id               INT(11)         NOT NULL REFERENCES t_stores (a_id),
    a_month                 DATE            NOT NULL,
    fifty_percent_notified  BOOLEAN         DEFAULT FALSE,
    hundred_percent_notified BOOLEAN        DEFAULT FALSE,
    PRIMARY KEY (a_store_id, a_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create Trigger to reset notifications after a allowance change

CREATE TRIGGER reset_notifications_after_allowance_change
BEFORE UPDATE ON t_allowances
FOR EACH ROW 
BEGIN
    IF OLD.a_allowance_amount != NEW.a_allowance_amount THEN
        UPDATE t_notifications
        SET fifty_percent_notified = FALSE, 
            hundred_percent_notified = FALSE
        WHERE a_store_id = NEW.a_store_id AND a_month = NEW.a_month;
    END IF;
END;


CREATE DATABASE IF NOT EXISTS test_store_allowances;
USE test_store_allowances;


-- GRANT ALL PRIVILEGES ON *.* TO 'user'@'%';
-- FLUSH PRIVILEGES;