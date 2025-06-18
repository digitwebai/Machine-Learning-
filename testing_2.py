import getpass
import mysql.connector
from mysql.connector import Error

def write_to_gcloud_database(host, port, user, password, database, table_name, data):
    """
    Connect to a Google Cloud SQL MySQL database using SSL certificates and write data.
   
    Parameters:
    - host (str): The database host (e.g., '34.118.200.124')
    - port (str): The database port (e.g., '3306')
    - user (str): The database username (e.g., 'root')
    - password (str): The database password (prompted if not provided)
    - database (str): The database name (e.g., 'amazon-competitor-profile')
    - table_name (str): The name of the table to write to
    - data (list of dict): List of dictionaries containing the data to insert
    - ssl_ca (str): Path to the server CA certificate
    - ssl_cert (str): Path to the client certificate
    - ssl_key (str): Path to the client private key
   
    Returns:
    - bool: True if the write operation is successful, False otherwise
    """
    connection = None
    cursor = None
   
    # # Verify SSL certificate files exist
    # for cert_file, cert_name in [(ssl_ca, "CA"), (ssl_cert, "Client Certificate"), (ssl_key, "Client Key")]:
    #     if not os.path.exists(cert_file):
    #         print(f"Error: {cert_name} file not found at {cert_file}")
    #         return False
   
    try:
        # Prompt for password if not provided
        if not password:
            password = getpass.getpass("Enter MySQL password for user 'root': ")
 
        # # SSL configuration
        # ssl_config = {
        #     'ssl_ca': ssl_ca,
        #     'ssl_cert': ssl_cert,
        #     'ssl_key': ssl_key,
        #     'ssl_verify_cert': True
        # }
       
        print(f"Attempting to connect to {host}:{port} as {user}...")
       
        # Establish connection to the database
        connection = mysql.connector.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            # **ssl_config
        )
       
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"Connected to database: {record[0]}")
           
            # Prepare the INSERT query dynamically based on the data
            if not data:
                print("No data provided to insert.")
                return False
           
            columns = list(data[0].keys())
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
           
            values = [tuple(item[col] for col in columns) for item in data]
           
            cursor.executemany(query, values)
            connection.commit()
            print(f"Successfully inserted {cursor.rowcount} rows into {table_name}.")
            return True
           
    except Error as e:
        print(f"Error while connecting to MySQL or writing data: {str(e)}")
        if "Access denied" in str(e):
            print("Please verify your username and password are correct.")
        elif "SSL connection" in str(e):
            print("SSL connection error. Please verify your SSL certificates are valid and properly configured.")
        return False
       
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")
 
# Example usage
if __name__ == "__main__":
    # Database connection parameters
    db_config = {
        "host": "34.118.200.124",
        "port": "3306",
        "user": "digitwebai",
        "password": "digitweb@2025",  # Replace with the actual root password or leave empty to prompt
        "database": "amazon-competitor-profile"
    }
   
    # Sample data to insert
    sample_data = [
    {"ASIN": "B07H8Q1V1C", "title": "Product A", "url_link": "https://www.amazon.com/dp/B07H8Q1V1C"},
    {"ASIN": "B08K9L2M3P", "title": "Product B", "url_link": "https://www.amazon.com/dp/B08K9L2M3P"}
]
   
    # # Paths to SSL certificates and key (using raw strings for Windows)
    # ssl_ca_path = r"D:\THIKSIGA\amazon_performance\server-ca.pem"
    # ssl_cert_path = r"D:\THIKSIGA\amazon_performance\client-cert.pem"
    # ssl_key_path = r"D:\THIKSIGA\amazon_performance\client-key.pem"
   
    # Write data to the 'products' table
    success = write_to_gcloud_database(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        table_name="competitor_products",
        data=sample_data,
        # ssl_ca=ssl_ca_path,
        # ssl_cert=ssl_cert_path,
        # ssl_key=ssl_key_path
    )
   
    if success:
        print("Data written successfully!")
    else:
        print("Failed to write data.")