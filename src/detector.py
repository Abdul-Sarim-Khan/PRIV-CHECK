#detector.py module
import re
from patterns import (
    PRIV_ESCALATION_PATTERNS,
    USER_MANAGEMENT_PATTERNS,
    FILE_PERMISSION_PATTERNS,
    SYSTEM_CONFIG_PATTERNS,
    DESTRUCTIVE_COMMAND_PATTERNS,
    INFO_COMMAND_PATTERNS,
    NETWORK_COMMAND_PATTERNS
)

def detect_patterns(script):
    """Detects high-privileged commands and classifies them by category"""
    matches = []
    found_types = set()

    # Remove comments but preserve commands
    cleaned_script = re.sub(r'//.*?$|/\*.*?\*/|#.*?$', '', script, flags=re.MULTILINE | re.DOTALL)
    
    # Check each pattern category
    categories = {
        'Privilege Escalation': PRIV_ESCALATION_PATTERNS,
        'User Management': USER_MANAGEMENT_PATTERNS,
        'File Permission': FILE_PERMISSION_PATTERNS,
        'System Config': SYSTEM_CONFIG_PATTERNS,
        'Destructive Command': DESTRUCTIVE_COMMAND_PATTERNS,
        'Sensitive Info Access': INFO_COMMAND_PATTERNS,
        'Network Admin': NETWORK_COMMAND_PATTERNS
    }
    
    for category, patterns in categories.items():
        for pattern in patterns:
            for match in re.finditer(pattern, cleaned_script, re.IGNORECASE):
                # Extract full command line
                line_start = cleaned_script.rfind('\n', 0, match.start()) + 1
                line_end = cleaned_script.find('\n', match.end())
                command = cleaned_script[line_start:line_end].strip()
                
                matches.append((category, command))
                found_types.add(category)

    return matches, found_types

def calculate_severity_and_tier(found_types):
    """Assigns severity score and tier based on command risk category"""
    if not found_types:
        return 0, "No Privileged Commands"
    
    severity_map = {
        'Destructive Command': 3,
        'Privilege Escalation': 3,
        'File Permission': 2,
        'System Config': 2,
        'User Management': 2,
        'Network Admin': 1,
        'Sensitive Info Access': 1
    }
    
    # Get highest severity level
    max_severity = max(severity_map.get(t, 0) for t in found_types)
    
    # Map to tier names
    tier_map = {
        0: "Clean",
        1: "Low Risk",
        2: "Medium Risk",
        3: "High Risk"
    }
    
    return max_severity, tier_map.get(max_severity, "Unknown")