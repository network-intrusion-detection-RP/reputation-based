import requests
import json


class IpGeoLocationTracker:
    """
    A class to track IP address information using the IPWHOIS API.

    Attributes:
        ip (str): The IP address to track.
        ip_data (dict): A dictionary containing information about the IP address (if successful).
    """

    def __init__(self, ip="136.233.9.98"):
        """
        Initializes the IPTracker object.

        Args:
            ip (str): The IP address to track. Default is "136.233.9.98".
        """

        self.ip = ip
        self.ip_data = None

        self.track_ip()

    def track_ip(self):
        """
        Fetches information about the IP address using the IPWHOIS API.
        """
        try:
            req_api = requests.get(f"http://ipwho.is/{self.ip}")
            req_api.raise_for_status()  # Raise exception for failed requests
            self.ip_data = json.loads(req_api.text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching IP information: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")

        # Access data only if ip_data is populated
        if self.ip_data:
            self.process_ip_data()

    def process_ip_data(self):
        # Extract data from ip_data using get method to handle missing keys
        self.type = self.ip_data.get("type")
        self.country = self.ip_data.get("country")
        self.country_code = self.ip_data.get("country_code")
        self.city = self.ip_data.get("city")
        self.continent = self.ip_data.get("continent")
        self.continent_code = self.ip_data.get("continent_code")
        self.region = self.ip_data.get("region")
        self.region_code = self.ip_data.get("region_code")
        self.latitude = self.ip_data.get("latitude")
        self.longitude = self.ip_data.get("longitude")
        self.is_eu = self.ip_data.get("is_eu")
        self.postal = self.ip_data.get("postal")
        self.calling_code = self.ip_data.get("calling_code")
        self.capital = self.ip_data.get("capital")
        self.borders = self.ip_data.get("borders")
        self.country_flag = self.ip_data.get("flag", {}).get("emoji")
        self.asn = self.ip_data.get("connection", {}).get("asn")
        self.org = self.ip_data.get("connection", {}).get("org")
        self.isp = self.ip_data.get("connection", {}).get("isp")
        self.domain = self.ip_data.get("connection", {}).get("domain")
        self.timezone_id = self.ip_data.get("timezone", {}).get("id")
        self.timezone_abbr = self.ip_data.get("timezone", {}).get("abbr")
        self.timezone_is_dst = self.ip_data.get("timezone", {}).get("is_dst")
        self.timezone_offset = self.ip_data.get("timezone", {}).get("offset")
        self.timezone_utc = self.ip_data.get("timezone", {}).get("utc")
        self.current_time = self.ip_data.get("timezone", {}).get("current_time")


if __name__ == "__main__":
    # Usage:
    ip_tracker = IpGeoLocationTracker()
    ip_tracker.track_ip()

    # Accessing individual attributes
    print(ip_tracker.type)
    print(ip_tracker.country)


