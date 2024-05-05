# IP Reputation Manager

A reputation manager for IP addresses. It leverages IP geolocation data and user-defined rules to assign reputation scores to IPs. Higher scores indicate a more trustworthy IP address.



## Components

**1. IpGeoLocationTracker:**

* **Purpose:** This class retrieves information about an IP address using an external API (IPWHOIS in this case).
* **Functionality:**
    * Takes an IP address as input (default is provided).
    * Uses the `requests` library to make an API call to IPWHOIS.
    * Parses the JSON response from the API to extract relevant data.
    * Stores the extracted data in a dictionary (`ip_data`). This data may include:
        * Country
        * Region
        * City
        * Continent
        * ISP (Internet Service Provider)
        * Organization
        * Timezone details
    * Handles potential errors during the API call or data parsing.

**2. PointRuleBuilder:**

* **Purpose:** This class helps define rules for assigning reputation points based on specific IP address attributes and their values.
* **Functionality:**
    * Provides methods to:
        * Specify the attribute to create a rule for (e.g., country, city).
        * Define point values for specific attribute values (e.g., 10 points for US, 5 points for Canada).
        * Optionally, create rules that apply to any value of an attribute (e.g., award 2 points for any European country).
    * Validates attribute names to ensure they correspond to the data retrieved by `IpGeoLocationTracker`.
    * Allows building and saving rules to a JSON file for later use.
    * Supports cloning existing rules for quick modification.
    * Enables grouping rules for easier management (optional).

**3. ReputationManager:**

* **Purpose:** This class is the core component that calculates an IP address's reputation score.
* **Functionality:**
    * Maintains a blacklist of malicious IPs (initially empty, can be customized).
    * Holds a set of point rules (default rules provided, can be loaded from JSON).
    * Takes an IP address as input.
    * Checks if the IP is blacklisted. If blacklisted, the reputation score is automatically 0.
    * If not blacklisted:
        * Creates an `IpGeoLocationTracker` object and retrieves the IP's geolocation data.
        * Iterates through the defined point rules.
        * For each rule, checks if the extracted IP data matches the rule's attribute and value.
            * If there's a match, adds the rule's assigned points to the reputation score.
    * Returns the final reputation score (higher score indicates a better reputation).



**Usage:**

1.  **Import necessary libraries:**

```python
import requests
import json
from collections import defaultdict
```

2.  **Create a ReputationManager object (optional with custom rules):**

```python
# Default rules
reputation_manager = ReputationManager()

# Custom rules loaded from JSON
custom_point_rules = ReputationManager.load_rules_from_json("custom_rules.json")
reputation_manager = ReputationManager(point_rules=custom_point_rules)
```

3.  **Get reputation score for an IP address:**

```python
ip_address = "8.8.8.8"
reputation_score = reputation_manager.get_reputation(ip_address)
print(f"Reputation score for {ip_address}: {reputation_score}")
```

**Further Customization:**

- Modify the `DEFAULT_POINT_RULES` dictionary in `ReputationManager` to set your desired point allocation for different IP attributes and values.
- Create custom point rules using `PointRuleBuilder` and save them to a JSON file for persistent use.
- Integrate this code with your application to filter or prioritize requests based on IP reputation scores.
 
