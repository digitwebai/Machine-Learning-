from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import pymysql
import datetime
import os
import ssl

# Your credentials and Cloud SQL details
CUSTOMER_ID = '4503486236'  # Your Google Ads Customer ID
DEVELOPER_TOKEN = '8xG5VbKfJ0ue0bN5JAvPyw'  # Your Developer Token
CLOUD_SQL_CONNECTION_NAME = 'uplifted-stream-461211-h8:us-central1:digitwebai'  # Your Cloud SQL instance connection name
DB_USER = 'digitwebai'  # Your Cloud SQL username
DB_PASSWORD = os.environ['DB_PASSWORD']  # Require environment variable for DB password
DB_NAME = 'ADS'  # Your Cloud SQL database name
DB_HOST = '34.118.200.124'  # Use public IP for Cloud SQL
DB_PORT = 3306  # Default TCP database port from the image

def fetch_google_ads_data():
    # Initialize the Google Ads client
    try:
        # Check if using google-ads.yaml or revert to default (client.json/pkl)
        client = GoogleAdsClient.load_from_storage("google-ads.yaml")  # Specify your credential file
    except FileNotFoundError:
        print("google-ads.yaml not found. Falling back to default credentials.")
        client = GoogleAdsClient.load_from_storage()  # Uses client.json or pkl from OAuth

    # Create a GoogleAdsService client
    googleads_service = client.get_service("GoogleAdsService")

    # Construct the GAQL query
    query = """
        SELECT
        campaign_budget.amount_micros,
        segments.date,
        campaign.id,
        campaign.name,
        metrics.ctr,
        metrics.conversions_value,
        metrics.cost_micros,
        metrics.conversions,
        metrics.clicks,
        metrics.impressions,
        metrics.all_conversions_value,
        metrics.cost_per_conversion,
        metrics.cost_per_all_conversions,
        metrics.value_per_conversion
        FROM campaign
        WHERE
        segments.date BETWEEN '2024-06-13' AND '2025-06-13'
        AND campaign.status = ENABLED
      """

    data = []
    try:
        # Issue the search request
        response = googleads_service.search(
            customer_id=CUSTOMER_ID,
            query=query
        )

        # Collect data
        for row in response:
            campaign = row.campaign
            metrics = row.metrics
            data.append((
                campaign.id,
                campaign.name,
                metrics.clicks or 0,  # Handle None values
                metrics.impressions or 0,
                metrics.cost_micros or 0,
                datetime.datetime.now()  # Add timestamp for record
            ))
        return data

    except GoogleAdsException as ex:
        print(f"An error occurred: {ex}")
        for error in ex.failure.errors:
            print(f"Error with message: {error.message}")
        return []

def setup_database():
    # Connect to Cloud SQL MySQL database
    print(f"Attempting connection to {DB_HOST}:{DB_PORT} as {DB_USER} with DB {DB_NAME}")
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            # Uncomment and configure the following lines if SSL is required
            ssl={
                'ca': r'C:\ML\server-ca.pem',
                'check_hostname': False,
                'verify_mode': 0  # 0 means CERT_NONE
            }  
        )
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaign_metrics (
                campaign_id BIGINT,
                campaign_name VARCHAR(255),
                clicks INT,
                impressions INT,
                cost_micros BIGINT,
                timestamp DATETIME,
                PRIMARY KEY (campaign_id, timestamp)
            )
        """)
        conn.commit()
        return conn, cursor
    except pymysql.Error as e:
        print(f"Database connection error: {e}")
        return None, None

def load_data_to_database(data, conn, cursor):
    if data and conn and cursor:
        try:
            # Insert data into the table
            insert_query = """
                INSERT INTO campaign_metrics (campaign_id, campaign_name, clicks, impressions, cost_micros, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                campaign_name=VALUES(campaign_name),
                clicks=VALUES(clicks),
                impressions=VALUES(impressions),
                cost_micros=VALUES(cost_micros),
                timestamp=VALUES(timestamp)
            """
            cursor.executemany(insert_query, data)
            conn.commit()
            print(f"Inserted {len(data)} records into Cloud SQL.")
        except pymysql.Error as e:
            print(f"Insert error: {e}")
            conn.rollback()
    else:
        print("No data or database connection to insert.")

def main():
    # Fetch data from Google Ads
    print("Fetching data from Google Ads...")
    ads_data = fetch_google_ads_data()

    # Set up database connection
    print("Setting up database connection to Cloud SQL...")
    conn, cursor = setup_database()

    # Load data into Cloud SQL
    print("Loading data into Cloud SQL...")
    load_data_to_database(ads_data, conn, cursor)

    # Close the connection
    if conn:
        conn.close()
        print("Pipeline completed.")

if __name__ == "__main__":
    main()