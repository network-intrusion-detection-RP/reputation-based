from ReputationManager import ReputationManager

if __name__ == '__main__':
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
        # Get reputation score for the IP address
        reputation_score = reputation_manager.get_reputation(ip_address)
        print(f"Reputation score for IP address {ip_address}: {reputation_score}")
