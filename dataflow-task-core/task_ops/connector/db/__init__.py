import certifi
import psycopg2
from pymongo import MongoClient

from task_ops.base import logutils
from task_ops.base.secrets import AwsSecretManagerVault
from task_ops.connector import Connector
from task_ops.exceptions import IllegalStateException

log = logutils.get_logger(__name__)


class MongoRepository(Connector):
    def __init__(self, name: str = "mongodb", region_name: str = None):
        super().__init__(name)
        self.secret_id = self.get_setting("mongo_secret_id")
        self.region_name = region_name
        self.mongo_uri = self.get_mongo_uri()
        if not self.mongo_uri:
            raise IllegalStateException("No MongoDB connection URI specified.")
        self.mongodb_client = MongoClient(self.mongo_uri, tlsCAFile=certifi.where())
        self.db = self.mongodb_client[self.get_setting("dbname")]

    def get_mongo_uri(self) -> str:
        if self.secret_id:
            vault = AwsSecretManagerVault(region_name=self.region_name)
            return vault.get_secret(self.secret_id, attr="mongoURI")

    def insert_document(self, collection_name: str, document: dict):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            log.debug("Document inserted successfully: %s", result.inserted_id)
        except Exception as e:
            log.error("Error inserting document: %s", str(e))
        finally:
            self.mongodb_client.close()

    def update_document(self, collection_name: str, query: dict, update: dict):
        try:
            collection = self.db[collection_name]
            result = collection.update_many(query, update)
            log.debug("Documents updated successfully: %d", result.modified_count)
        except Exception as e:
            log.error("Error updating documents: %s", str(e))
        finally:
            self.mongodb_client.close()

    def find_documents(self, collection_name: str, query: dict):
        try:
            collection = self.db[collection_name]
            result = collection.find(query)
            return list(result)
        except Exception as e:
            log.error("Error finding documents: %s", str(e))
        finally:
            self.mongodb_client.close()

    def find_one_document(self, collection_name: str, query: dict):
        try:
            collection = self.db[collection_name]
            result = collection.find_one(query)
            return result
        except Exception as e:
            log.error("Error finding document: %s", str(e))
        finally:
            self.mongodb_client.close()

    def delete_documents(self, collection_name: str, query: dict):
        try:
            collection = self.db[collection_name]
            result = collection.delete_many(query)
            log.debug("Documents deleted successfully: %d", result.deleted_count)
        except Exception as e:
            log.error("Error deleting documents: %s", str(e))
        finally:
            self.mongodb_client.close()


class PostgresRepository(Connector):
    def __init__(self, name: str = "postgresdb", region_name: str = None):
        super().__init__(name)
        self.secret_id = self.get_setting("postgres_secret_id")
        self.region_name = region_name
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = self.get_postgres_connection()
            self.cursor = self.connection.cursor()
        except Exception as e:
            log.error("Error connecting to PostgreSQL: %s", str(e))

    def get_postgres_connection(self):
        if self.secret_id:
            vault = AwsSecretManagerVault(region_name=self.region_name)
            secrets = vault.get_secret(self.secret_id)
            db_url = secrets["url"]
            username = secrets["username"]
            password = secrets["password"]
        else:
            db_url = self.get_setting("url")
            username = self.get_setting("username")
            password = self.get_setting("password")
        return psycopg2.connect(
            dbname=db_url,
            user=username,
            password=password
        )

    def execute_query(self, query: str, params: tuple = None):
        try:
            if not self.connection or self.connection.closed:
                self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            log.debug("Query executed successfully: %s", query)
        except Exception as e:
            log.error("Error executing query: %s", str(e))
        finally:
            self.close_connection()

    def insert(self, table_name: str, data: dict):
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.execute_query(query, tuple(data.values()))
            log.debug("Data inserted successfully into %s", table_name)
        except Exception as e:
            log.error("Error inserting data into %s: %s", table_name, str(e))

    def update(self, table_name: str, data: dict, condition: str):
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            self.execute_query(query, tuple(data.values()))
            log.debug("Data updated successfully in %s", table_name)
        except Exception as e:
            log.error("Error updating data in %s: %s", table_name, str(e))

    def fetch_all(self, table_name: str, condition: str = None):
        try:
            query = f"SELECT * FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            log.error("Error fetching data from %s: %s", table_name, str(e))
        finally:
            self.close_connection()

    def fetch_one(self, table_name: str, condition: str):
        try:
            query = f"SELECT * FROM {table_name} WHERE {condition}"
            self.cursor.execute(query)
            return self.cursor.fetchone()
        except Exception as e:
            log.error("Error fetching one data from %s: %s", table_name, str(e))
        finally:
            self.close_connection()

    def delete(self, table_name: str, condition: str):
        try:
            query = f"DELETE FROM {table_name} WHERE {condition}"
            self.execute_query(query)
            log.debug("Data deleted successfully from %s", table_name)
        except Exception as e:
            log.error("Error deleting data from %s: %s", table_name, str(e))

    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            log.debug("PostgreSQL connection closed.")
        except Exception as e:
            log.error("Error closing connection: %s", str(e))


def main(db_type):
    if db_type.lower() == "mongo":
        # Example usage for MongoRepository
        mongo_repo = MongoRepository()
        collection_name = "your_collection_name"
        document = {"key": "value"}
        mongo_repo.insert_document(collection_name, document)
    elif db_type.lower() == "postgres":
        # Example usage for PostgresRepository
        postgres_repo = PostgresRepository()
        table_name = "your_table"
        data = {"column1": "value1", "column2": "value2"}
        postgres_repo.insert(table_name, data)
        rows = postgres_repo.fetch_all(table_name)
        print("Postgres data:")
        print(rows)
        postgres_repo.close_connection()
    else:
        print("Invalid database type provided.")


if __name__ == "__main__":
    db_type = "postgres"
    main(db_type)
