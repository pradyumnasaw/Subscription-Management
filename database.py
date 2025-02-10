import sqlite3
import csv

def get_db_connection():
    try:
        conn = sqlite3.connect('mem_management.db')
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table():
    try:
        conn = get_db_connection()
        if conn is None:
            return
        cur = conn.cursor()
        member_table = '''
            CREATE TABLE IF NOT EXISTS member (
                mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                mobile TEXT NOT NULL,
                email TEXT,
                mem_type TEXT CHECK (mem_type IN ('Monthly', 'Quarterly', 'Yearly')),
                status TEXT CHECK (status IN ('Activate', 'Deactivate')) DEFAULT 'Activate',
                start_date DATE DEFAULT CURRENT_DATE,
                end_date DATE
            )
        '''
        payment_table = '''
            CREATE TABLE IF NOT EXISTS payment (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                mem_id INTEGER REFERENCES member(mem_id),
                amount DECIMAL(10, 2) NOT NULL,
                payment_date DATE DEFAULT CURRENT_DATE
            )
        '''
        cur.execute(member_table)
        cur.execute(payment_table)
        conn.commit()
        cur.close()
        conn.close()
        print('Tables created or already exist.')
    except Exception as e:
        print(f"Error creating table: {e}")

def add_member(mem_info):
    try:
        conn = get_db_connection()
        if conn is None:
            return
        cur = conn.cursor()
        new_member = '''
            INSERT INTO member (name, mobile, email, mem_type, start_date, end_date) 
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        cur.execute(new_member, (
            mem_info["name"], mem_info["mobile"], mem_info["email"], 
            mem_info["mem_type"], mem_info["start_date"], mem_info["end_date"]
        ))
        conn.commit()
        cur.close()
        conn.close()
        print("Member added successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error adding member: {e}")

def update_member(update_info):
    try:
        conn = get_db_connection()
        if conn is None:
            return
        cur = conn.cursor()
        mem_update = '''UPDATE member 
                        SET mobile = ?, email = ?, mem_type = ? 
                        WHERE mem_id = ?'''
        
        cur.execute(mem_update, (update_info["mobile"], update_info["email"], update_info["mem_type"], update_info["id"]))
        conn.commit()
        cur.close()
        conn.close()
        print("Member updated successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error updating member: {e}")

def update_status(update_status_info):
    try:
        conn = get_db_connection()
        if conn is None:
            return
        cur = conn.cursor()
        update_sta = '''UPDATE member 
                        SET status = ?
                        WHERE mem_id = ?'''
        cur.execute(update_sta, (update_status_info["act_deact"], update_status_info["id"]))
        conn.commit()
        cur.close()
        conn.close()
        print("Member status updated successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error updating member status: {e}")

def get_all_members(filters=None):
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        query = 'SELECT * FROM member'
        params = []
        if filters:
            conditions = []
            if 'status' in filters:
                conditions.append('status = ?')
                params.append(filters['status'])
            if 'mem_type' in filters:
                conditions.append('mem_type = ?')
                params.append(filters['mem_type'])
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
        cur.execute(query, params)
        records = cur.fetchall()
        cur.close()
        conn.close()
        return records
    except Exception as e:
        print(f"Error fetching members: {e}")
        return []

def search_members(search_by, search_value):
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        query = '''
            SELECT * FROM member 
            WHERE name LIKE ? OR email LIKE ? OR mem_type LIKE ?
        '''
        search_pattern = f"%{search_value}%"
        cur.execute(query, (search_pattern, search_pattern, search_pattern))
        records = cur.fetchall()
        cur.close()
        conn.close()
        return records
    except Exception as e:
        print(f"Error searching members: {e}")
        return []

def record_payment(payment_info):
    try:
        conn = get_db_connection()
        if conn is None:
            return
        cur = conn.cursor()
        new_payment = '''
            INSERT INTO payment (mem_id, amount, payment_date) 
            VALUES (?, ?, ?)
        '''
        cur.execute(new_payment, (
            payment_info["mem_id"], payment_info["amount"], payment_info["payment_date"]
        ))
        conn.commit()
        cur.close()
        conn.close()
        print("Payment recorded successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Error recording payment: {e}")

def get_payment_history(mem_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        query = 'SELECT * FROM payment WHERE mem_id = ?'
        cur.execute(query, (mem_id,))
        records = cur.fetchall()
        cur.close()
        conn.close()
        return records
    except Exception as e:
        print(f"Error fetching payment history: {e}")
        return []

def get_upcoming_renewals(days=30):
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        query = '''
            SELECT * FROM member 
            WHERE end_date BETWEEN DATE('now') AND DATE('now', ? || ' days')
        '''
        cur.execute(query, (days,))
        records = cur.fetchall()
        cur.close()
        conn.close()
        return records
    except Exception as e:
        print(f"Error fetching upcoming renewals: {e}")
        return []

def download_reports(file_path):
    try:
        conn = get_db_connection()
        if conn is None:
            return
        cur = conn.cursor()
        query = 'SELECT * FROM member'
        cur.execute(query)
        records = cur.fetchall()
        cur.close()
        conn.close()
        
        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['mem_id', 'name', 'mobile', 'email', 'mem_type', 'status', 'start_date', 'end_date'])
            csvwriter.writerows(records)
        print(f"Report downloaded successfully to {file_path}.")
    except Exception as e:
        print(f"Error downloading report: {e}")

def export_data():
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cur = conn.cursor()
        query = 'SELECT * FROM member'
        cur.execute(query)
        records = cur.fetchall()
        cur.close()
        conn.close()
        return records
    except Exception as e:
        print(f"Error exporting data: {e}")
        return []

# Initialize Database
create_table()
