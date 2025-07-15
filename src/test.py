# test.py (for manual testing)

from detector import detect_patterns, calculate_severity_and_tier


script = """
<script>alert('hello')</script>
SELECT * FROM users WHERE name = 'admin' -- 
rm -rf /home/user
"""

matches, found_types = detect_patterns(script)  # <-- FIX: unpack the tuple
severity, tier = calculate_severity_and_tier(found_types)

print("Matches:", matches)
print("Severity:", severity)
print("Risk Tier:", tier)