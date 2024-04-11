from IPGeoLocationTracker import IpGeoLocationTracker


class ReputationManager:
    BLACKLIST: set[str] = {"Blacklisted IPs"}  # Class attribute (default blacklist)
    DEFAULT_POINT_RULES = {
        "country": {"US": 10, "UK": 20},
        "region": {"NY": 5, "CA": 8},
        "city": {"New York City": 5, "Los Angeles": 8},
        "isp": {"ISP1": 10, "ISP2": 15},
        "org": {"Organization1": 10, "Organization2": 15}
    }

    def __init__(self, blacklist: set | None = None, point_rules: dict | None = None):
        """
        Initializes a ReputationManager object.

        Args:
            blacklist (set, optional): A set of IP addresses to blacklist.
                If None, the class-level BLACKLIST will be used.
            point_rules (dict, optional): A dictionary containing rules for assigning points based on attributes.
                If None, the class-level DEFAULT_POINT_RULES will be used.

        Returns:
            ReputationManager: A new ReputationManager object.
        """

        if blacklist is None:
            self.blacklist = self.BLACKLIST.copy()  # Use class attribute if no argument provided
        else:
            self.blacklist = blacklist

        if point_rules is None:
            self.point_rules = self.DEFAULT_POINT_RULES.copy()  # Use class attribute if no argument provided
        else:
            self.point_rules = point_rules

    def get_reputation(self, ip_address: str) -> int:
        """
        Calculates the reputation score for the given IP address.

        Args:
            ip_address (str): The IP address to calculate reputation for.

        Returns:
            int: The reputation score.
        """
        if self.check_in_blacklist(ip_address):
            return 0  # IP is blacklisted, reputation score is 0

        # Create a new IpGeoLocationTracker object to track the IP address
        ip_tracker = IpGeoLocationTracker(ip_address)
        ip_tracker.track_ip()

        # Calculate reputation based on point rules
        reputation_score = 0
        for attr, attr_rules in self.point_rules.items():
            attr_value = getattr(ip_tracker, attr)
            if attr_value in attr_rules:
                reputation_score +=attr_rules[attr_value]
            pass

        return reputation_score

    def check_in_blacklist(self, ip_address: str) -> bool:
        """
        Checks if the given IP address is in the blacklist.

        Args:
            ip_address (str): The IP address to check.

        Returns:
            bool: True if IP address is in the blacklist, False otherwise.
        """
        return ip_address in self.blacklist


if __name__ == "__main__":
    # Define custom point rules
    custom_point_rules = {
        "country": {"United States": 10, "UK": 20, "India": 100},
        "region": {"NY": 5, "CA": 8},
        "city": {"New York City": 5, "Los Angeles": 8},
        "isp": {"ISP1": 10, "ISP2": 15},
        "org": {"Organization1": 10, "Organization2": 15}
    }

    # Initialize ReputationManager with custom point rules
    reputation_manager = ReputationManager(point_rules=custom_point_rules)

    # Example IP addresses to calculate reputation for
    ip_addresses = ["136.233.9.98", "8.8.8.8"]

    for ip_address in ip_addresses:
        # Get reputation score for the IP addrsss
        reputation_score = reputation_manager.get_reputation(ip_address)
        print(f"Reputation score for IP address {ip_address}: {reputation_score}")
