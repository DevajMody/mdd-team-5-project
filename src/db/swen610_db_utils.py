import psycopg2
import yaml
import os

def load_config():
    config = {}
    yml_path = os.path.join(os.path.dirname(__file__), "../../config/db.yml")
    with open(yml_path, "r") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config

def connect():
    # Load configuration from db.yml
    config = load_config()
    
    # Use environment variables if available, otherwise use config from yml
    return psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB', config["database"]),
        user=os.getenv('POSTGRES_USER', config["user"]),
        password=os.getenv('POSTGRES_PASSWORD', config["password"]),
        host=os.getenv('POSTGRES_HOST', config["host"]),
        port=os.getenv('POSTGRES_PORT', config["port"]),
    )

def exec_sql_file(path):
    full_path = os.path.join(os.path.dirname(__file__), f"../../{path}")
    conn = connect()
    cur = conn.cursor()
    with open(full_path, "r") as file:
        cur.execute(file.read())
    conn.commit()
    cur.close()
    conn.close()

def exec_get_one(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    one = cur.fetchone()
    cur.close()
    conn.close()
    return one

def exec_get_all(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    list_of_tuples = cur.fetchall()
    cur.close()
    conn.close()
    return list_of_tuples

def exec_commit(sql, args={}):
    conn = connect()
    cur = conn.cursor()
    result = cur.execute(sql, args)
    conn.commit()
    cur.close()
    conn.close()
    return result
