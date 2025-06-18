from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Replace with your customer ID and developer token
CUSTOMER_ID = '4503486236'  # e.g., '123-456-7890'
DEVELOPER_TOKEN = '8xG5VbKfJ0ue0bN5JAvPyw'

def main():
    # Initialize the Google Ads client using the client.json from the installed app setup
    client = GoogleAdsClient.load_from_storage("google-ads.yaml")

    # Create a GoogleAdsService client
    googleads_service = client.get_service("GoogleAdsService")

    # Construct the GAQL query
    query = """
        SELECT campaign.id, campaign.name, metrics.clicks, metrics.impressions, metrics.cost_micros
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS
    """

    try:
        # Issue the search request
        response = googleads_service.search(
            customer_id=CUSTOMER_ID,
            query=query
        )

        # Iterate over the results and print them
        for row in response:
            campaign = row.campaign
            metrics = row.metrics
            print(f"Campaign ID: {campaign.id}, Name: {campaign.name},Clicks: {metrics.clicks} Impressions: {metrics.impressions}")
            print(f"Cost (micros): {metrics.cost_micros}, Cost ($): {metrics.cost_micros / 1000000:.2f}")
            print("---")

    except GoogleAdsException as ex:
        print(f"An error occurred: {ex}")
        for error in ex.failure.errors:
            print(f"Error with message: {error.message}")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\tOn field: {field_path_element.field_name}")

if __name__ == "__main__":
    main()