import psycopg2

def connect_database():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="emr_project",
            user="postgres",
            password="********"
        )

        print("✅ Connected to PostgreSQL successfully!")
        return connection

    except Exception as e:
        print("❌ Error:", e)
        return None