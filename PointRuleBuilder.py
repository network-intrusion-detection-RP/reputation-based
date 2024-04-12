from collections import defaultdict
import json
from typing import Callable


class PointRule:
    """
    Represents a rule for awarding points based on attribute and value.
    """

    def __init__(self, attribute: str, value: str | None = None, points: int = 0):
        """
        Initialize a PointRule instance.

        Args:
            attribute (str): The attribute to which the rule applies.
            value (str | None): The value of the attribute (optional).
            points (int): The points awarded for the attribute-value combination.
        """
        self.attribute = attribute
        self.value = value
        self.points = points

    def __str__(self):
        """
        Return a string representation of the PointRule.

        Returns:
            str: String representation of the PointRule.
        """
        if self.value:
            return f"Award {self.points} points for {self.attribute} with value '{self.value}'"
        else:
            return f"Award {self.points} points for any value of {self.attribute}"


class PointRuleBuilder:
    """
    Builds and manages rules for awarding points.
    """

    VALID_ATTRIBUTES: set[str] = {
        "country", "country_code", "city", "continent", "continent_code",
        "region", "region_code", "latitude", "longitude", "is_eu",
        "postal", "calling_code", "capital", "borders", "country_flag",
        "asn", "org", "isp", "domain", "timezone_id", "timezone_abbr",
        "timezone_is_dst", "timezone_offset", "timezone_utc", "current_time"
    }

    def __init__(self):
        """
        Initialize a PointRuleBuilder instance.
        """
        self.rules = []
        self.rule_groups: dict[str, list[PointRule]] = defaultdict(list)

    # VALIDATION FUNCTIONS
    def validate_attribute_name(self, attribute_name: str) -> bool:
        """
        Validate the provided attribute name.

        Args:
            attribute_name (str): The attribute name to validate.

        Returns:
            bool: True if the attribute name is valid, False otherwise.
        """
        return attribute_name in PointRuleBuilder.VALID_ATTRIBUTES

    # BUILDER

    def for_attribute(self, attribute: str):
        """
        Begin building rules for the specified attribute.

        Args:
            attribute (str): The attribute to build rules for.

        Returns:
            PointRuleBuilder: The current instance of PointRuleBuilder.
        """
        if self.validate_attribute_name(attribute_name=attribute):
            self.current_attribute = attribute
            self.current_values = []
        else:
            print(f"Error: '{attribute}' is not a valid attribute.")
        return self

    def with_value(self, *values: str):
        """
        Add values to the current attribute being built.

        Args:
            values (str): Values to add to the current attribute.

        Returns:
            PointRuleBuilder: The current instance of PointRuleBuilder.
        """
        self.current_values.extend(values)
        return self

    def with_points(self, points: int):
        """
        Set the points for the current attribute-value combination.

        Args:
            points (int): Points to assign to the current attribute-value combination.

        Returns:
            PointRuleBuilder: The current instance of PointRuleBuilder.
        """
        try:
            if points < 0:
                raise ValueError("Points must be a non-negative integer.")
            for value in self.current_values:
                self.rules.append(
                    PointRule(self.current_attribute, value, points))
        except ValueError as e:
            print(f"Error: {e}")
        return self

    def build(self):
        """
        Build and return the list of rules.

        Returns:
            list[PointRule]: The list of rules.
        """
        return self.rules

    def clone_rule(self, index: int):
        """
        Clone an existing rule at the specified index.

        Args:
            index (int): The index of the rule to clone.

        Returns:
            PointRuleBuilder: A new instance of PointRuleBuilder with the cloned rule added.
        """
        if 0 <= index < len(self.rules):
            cloned_builder = PointRuleBuilder()
            cloned_builder.rules = self.rules.copy()
            cloned_builder.rules.append(
                self.rules[index])  # Append the cloned rule
            return cloned_builder
        else:
            print("Error: Invalid rule index.")
            return None

    def add_rule_to_group(self, group_name: str, rule: PointRule):
        """
        Add a rule to a specific rule group.

        Args:
            group_name (str): The name of the rule group.
            rule (PointRule): The rule to be added to the group.
        """
        if group_name not in self.rule_groups:
            self.rule_groups[group_name] = []  # Initialize the group if it doesn't exist
        self.rule_groups[group_name].append(rule)

    def apply_operation_to_group(self, group_name: str, operation: Callable):
        """
        Apply a specified operation to all rules in a rule group.

        Args:
            group_name (str): The name of the rule group.
            operation (Callable): The operation to be applied to each rule.
        """
        if group_name in self.rule_groups:
            for rule in self.rule_groups[group_name]:
                operation(rule)
        else:
            print(f"Error: Rule group '{group_name}' not found.")

    # JSON SHIZ
    def save_to_json(self, filename: str = "custom_rules.json"):
        """
        Save the rules to a JSON file.

        Args:
            filename (str): The filename to save the rules to (default is 'custom_rules.json').
        """
        data = defaultdict(dict)
        
        # Add rules from self.rules
        for rule in self.rules:
            data[rule.attribute][rule.value] = rule.points
        
        # Add rules from rule groups
        for group_rules in self.rule_groups.values():
            for rule in group_rules:
                data[rule.attribute][rule.value] = rule.points
        
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Rules saved to '{filename}' successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def load_from_json(self, filename: str):
        """
        Load rules from a JSON file.

        Args:
            filename (str): The filename from which to load rules.
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            for attribute, value_points in data.items():
                for value, points in value_points.items():
                    self.for_attribute(attribute).with_value(
                        value).with_points(points)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    point_rule_builder = PointRuleBuilder()
    point_rule_builder.load_from_json("test.json")

    # Cloning a rule
    cloned_builder = point_rule_builder.clone_rule(0)  # Clone the rule at index 0

    # Adding rules to groups
    rule1 = PointRule("country", "US", 10)
    rule2 = PointRule("country", "UK", 98)
    point_rule_builder.add_rule_to_group("group1", rule1)  # Add rule1 to group1
    point_rule_builder.add_rule_to_group("group1", rule2)  # Add rule2 to group2

    # Applying an operation to a group
    def double_points(rule):
        rule.points *= 2

    point_rule_builder.apply_operation_to_group("group1", double_points)  # Double points for all rules in "group1"

    # Saving rules to JSON
    point_rule_builder.save_to_json("updated_rules.json")
