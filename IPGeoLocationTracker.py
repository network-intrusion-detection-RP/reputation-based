import requests
import json
import time


class IpGeoLocationTracker:
    """
    A class to track IP address information using the IPWHOIS API.

    Attributes:
        ip (str): The IP address to track.
        ip_data (dict): A dictionary containing information about the IP address.
        type (str): The type of IP address (e.g., "ipv4").
        country (str): The country associated with the IP address.
        country_code (str): The country code associated with the IP address.
        city (str): The city associated with the IP address.
        continent (str): The continent associated with the IP address.
        continent_code (str): The continent code associated with the IP address.
        region (str): The region associated with the IP address.
        region_code (str): The region code associated with the IP address.
        latitude (float): The latitude of the location associated with the IP address.
        longitude (float): The longitude of the location associated with the IP address.
        is_eu (bool): Indicates if the IP address is in the European Union.
        postal (str): The postal code associated with the IP address.
        calling_code (str): The calling code associated with the IP address.
        capital (str): The capital associated with the IP address.
        borders (list): A list of bordering countries associated with the IP address.
        country_flag (str): The flag emoji representing the country associated with the IP address.
        asn (str): The Autonomous System Number (ASN) associated with the IP address.
        org (str): The organization associated with the IP address.
        isp (str): The Internet Service Provider (ISP) associated with the IP address.
        domain (str): The domain associated with the IP address.
        timezone_id (str): The timezone ID associated with the IP address.
        timezone_abbr (str): The timezone abbreviation associated with the IP address.
        timezone_is_dst (bool): Indicates if the timezone is observing daylight saving time.
        timezone_offset (int): The timezone offset from UTC in seconds.
        timezone_utc (str): The UTC timezone associated with the IP address.
        current_time (str): The current time in the timezone associated with the IP address.
    """

    def __init__(self, ip="136.233.9.98"):
        """
        Initializes the IPTracker object.

        Args:
            ip (str): The IP address to track. Default is "136.233.9.98".
        """

        self.ip = ip
        self.ip_data = None
        self.type = None
        self.country = None
        self.country_code = None
        self.city = None
        self.continent = None
        self.continent_code = None
        self.region = None
        self.region_code = None
        self.latitude = None
        self.longitude = None
        self.is_eu = None
        self.postal = None
        self.calling_code = None
        self.capital = None
        self.borders = None
        self.country_flag = None
        self.asn = None
        self.org = None
        self.isp = None
        self.domain = None
        self.timezone_id = None
        self.timezone_abbr = None
        self.timezone_is_dst = None
        self.timezone_offset = None
        self.timezone_utc = None
        self.current_time = None

        # function calling
        self.track_ip()

    def track_ip(self):
        """
        Fetches information about the IP address using the IPWHOIS API.
        """
        req_api = requests.get(f"http://ipwho.is/{self.ip}")  # API IPWHOIS.IS
        self.ip_data = json.loads(req_api.text)
        if self.ip_data:
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
