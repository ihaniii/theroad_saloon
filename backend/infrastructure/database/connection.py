import sqlite3
from backend.infrastructure.configuration.config import AppConfig

class DbConnection:
    _sqlite_conn = None
    _postgres_conn = None

    @classmethod
    def get_connection(cls):
        # Read engine from configuration
        engine = AppConfig.DB_ENGINE
        
        if engine == "postgresql":
            import psycopg2  # Dynamic import to prevent crash on systems without psycopg2
            if cls._postgres_conn is None or cls._postgres_conn.closed:
                # Establish postgres connection
                cls._postgres_conn = psycopg2.connect(
                    user=AppConfig.POSTGRES_USER,
                    password=AppConfig.POSTGRES_PASSWORD,
                    host=AppConfig.POSTGRES_HOST,
                    port=AppConfig.POSTGRES_PORT,
                    database=AppConfig.POSTGRES_DB
                )
                cls.initialize_postgres_tables(cls._postgres_conn)
            return cls._postgres_conn
        else:
            if cls._sqlite_conn is None:
                cls._sqlite_conn = sqlite3.connect("file:theroad_test_db?mode=memory&cache=shared", uri=True)
                cls._sqlite_conn.row_factory = sqlite3.Row
                cls.initialize_sqlite_tables(cls._sqlite_conn)
            return cls._sqlite_conn

    @classmethod
    def initialize_sqlite_tables(cls, conn):
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            allergies TEXT DEFAULT '',
            preferred_beverage TEXT DEFAULT 'القهوة العربية',
            total_visits INTEGER DEFAULT 0,
            lifetime_value REAL DEFAULT 0.0,
            loyalty_points INTEGER DEFAULT 0,
            loyalty_tier TEXT DEFAULT 'عامة'
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            branch_id TEXT NOT NULL,
            is_suspended INTEGER DEFAULT 0
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointment (
            id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            employee_id TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            status TEXT NOT NULL,
            checked_in INTEGER DEFAULT 0,
            start_minute INTEGER NOT NULL,
            duration_minutes INTEGER NOT NULL,
            clean_buffer INTEGER DEFAULT 15,
            room_id TEXT DEFAULT 'main_room',
            chair_id TEXT DEFAULT 'chair_1'
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            sku TEXT DEFAULT '',
            reorder_point INTEGER DEFAULT 5,
            warehouse TEXT DEFAULT 'Main Store'
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice (
            id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            discount REAL DEFAULT 0.0,
            is_paid INTEGER DEFAULT 0,
            payment_method TEXT,
            refunded INTEGER DEFAULT 0
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id TEXT NOT NULL,
            item_name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """)
        conn.commit()

    @classmethod
    def initialize_postgres_tables(cls, conn):
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(100) NOT NULL,
            is_active INT DEFAULT 1,
            allergies TEXT DEFAULT '',
            preferred_beverage VARCHAR(255) DEFAULT 'القهوة العربية',
            total_visits INT DEFAULT 0,
            lifetime_value REAL DEFAULT 0.0,
            loyalty_points INT DEFAULT 0,
            loyalty_tier VARCHAR(100) DEFAULT 'عامة'
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            role VARCHAR(100) NOT NULL,
            branch_id VARCHAR(100) NOT NULL,
            is_suspended INT DEFAULT 0
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointment (
            id VARCHAR(100) PRIMARY KEY,
            customer_id VARCHAR(100) NOT NULL,
            employee_id VARCHAR(100) NOT NULL,
            time_slot VARCHAR(100) NOT NULL,
            status VARCHAR(100) NOT NULL,
            checked_in INT DEFAULT 0,
            start_minute INT NOT NULL,
            duration_minutes INT NOT NULL,
            clean_buffer INT DEFAULT 15,
            room_id VARCHAR(100) DEFAULT 'main_room',
            chair_id VARCHAR(100) DEFAULT 'chair_1'
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id VARCHAR(100) PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            quantity INT NOT NULL,
            sku VARCHAR(100) DEFAULT '',
            reorder_point INT DEFAULT 5,
            warehouse VARCHAR(100) DEFAULT 'Main Store'
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice (
            id VARCHAR(100) PRIMARY KEY,
            customer_id VARCHAR(100) NOT NULL,
            discount REAL DEFAULT 0.0,
            is_paid INT DEFAULT 0,
            payment_method VARCHAR(100),
            refunded INT DEFAULT 0
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_item (
            id SERIAL PRIMARY KEY,
            invoice_id VARCHAR(100) NOT NULL,
            item_name VARCHAR(255) NOT NULL,
            price REAL NOT NULL
        )
        """)
        conn.commit()
