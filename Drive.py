import sqlite3
from datetime import date

conn = sqlite3.connect('driver_payments.db')

conn.execute('''
    CREATE TABLE IF NOT EXISTS drivers (
        driver_id INTEGER PRIMARY KEY,
        driver_name TEXT
    )
''')

conn.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        driver_id INTEGER,
        driver_name TEXT,
        amount REAL,
        payment_date TEXT
    )
''')

def record_payment():
    choice = input("Enter 'id' to enter driver ID or 'name' to enter driver name: ")

    if choice == "id":
        driver_id = int(input("Enter the driver ID: "))
        cursor = conn.execute('''
            SELECT driver_name
            FROM drivers
            WHERE driver_id = ?
        ''', (driver_id,))
    elif choice == "name":
        driver_name = input("Enter the driver name: ")
        driver_name = driver_name.lower()
        cursor = conn.execute('''
            SELECT driver_id
            FROM drivers
            WHERE LOWER(driver_name) = ?
        ''', (driver_name,))
    else:
        print("Invalid choice. Please try again.")
        return

    row = cursor.fetchone()

    if row is None:
        if choice == "id":
            driver_name = input("Enter the driver name: ")
            conn.execute('''
                INSERT INTO drivers (driver_id, driver_name)
                VALUES (?, ?)
            ''', (driver_id, driver_name))
        else:
            driver_id = int(input("Enter the driver ID: "))
            conn.execute('''
                INSERT INTO drivers (driver_id, driver_name)
                VALUES (?, ?)
            ''', (driver_id, driver_name))
    else:
        driver_id, driver_name = row

    amount = float(input("Enter the payment amount: "))
    payment_date = input("Enter the payment date (YYYY-MM-DD): ")

    if payment_date == "":
        payment_date = str(date.today())

    conn.execute('''
        INSERT INTO payments (driver_id, driver_name, amount, payment_date)
        VALUES (?, ?, ?, ?)
    ''', (driver_id, driver_name, amount, payment_date))

    conn.commit()
    print("Payment recorded successfully.")

def check_missed_payments():
    choice = input("Enter 'id' to search by driver ID or 'name' to search by driver name: ")

    if choice == "id":
        driver_id = int(input("Enter the driver ID: "))
        cursor = conn.execute('''
            SELECT driver_name
            FROM drivers
            WHERE driver_id = ?
        ''', (driver_id,))
    elif choice == "name":
        driver_name = input("Enter the driver name: ")
        driver_name = driver_name.lower()
        cursor = conn.execute('''
            SELECT driver_name
            FROM drivers
            WHERE LOWER(driver_name) = ?
        ''', (driver_name,))
    else:
        print("Invalid choice. Please try again.")
        return

    row = cursor.fetchone()

    if row is None:
        print("Driver not found.")
        return

    driver_name = row[0]

    cursor = conn.execute('''
        SELECT payment_date
        FROM payments
        WHERE driver_id = ?
            AND payment_date <> ?
    ''', (driver_id, str(date.today())))

    missed_payment_dates = [row[0] for row in cursor.fetchall()]

    if missed_payment_dates:
        print("Missed payment(s) found on the following dates:")
        for date in missed_payment_dates:
            print(date)
    else:
        print("No missed payments.")

def check_total_payments():
    choice = input("Enter 'id' to search by driver ID or 'name' to search by driver name: ")

    if choice == "id":
        driver_id = int(input("Enter the driver ID: "))
        cursor = conn.execute('''
            SELECT SUM(amount)
            FROM payments
            WHERE driver_id = ?
        ''', (driver_id,))
    elif choice == "name":
        driver_name = input("Enter the driver name: ")
        driver_name = driver_name.lower()
        cursor = conn.execute('''
            SELECT SUM(amount)
            FROM payments
            WHERE LOWER(driver_name) = ?
        ''', (driver_name,))
    else:
        print("Invalid choice. Please try again.")
        return

    total_payments = cursor.fetchone()[0]
    print("Total payments: $", total_payments)

while True:
    print("\nMenu:")
    print("1. Record Payment")
    print("2. Check Missed Payments")
    print("3. Check Total Payments")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        record_payment()
    elif choice == "2":
        check_missed_payments()
    elif choice == "3":
        check_total_payments()
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please try again.")

conn.close()
