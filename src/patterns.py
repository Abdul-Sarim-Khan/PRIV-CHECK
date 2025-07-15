# src/patterns.py

# Privilege Escalation Commands
PRIV_ESCALATION_PATTERNS = [
    r"\bsudo\b",
    r"\bsu\s+root\b",
    r"\brunas\b",
    r"\bsetuid\b",
    r"\bdoas\b",    
]

# User Management Commands (Windows & Unix)
USER_MANAGEMENT_PATTERNS = [
    r"\badduser\b",
    r"\buseradd\b",
    r"\busermod\b",
    r"\bnet\s+user\b",
    r"\bnet\s+localgroup\b",
    r"\bdsadd\b",
    r"\bpasswd\b",
    r"\bgroupadd\b",
]

# File/Permission Modification
FILE_PERMISSION_PATTERNS = [
    r"\bchmod\s+[0-7]{3,4}\b",  # Any chmod with 3-4 digit permission
    r"\bchown\b",
    r"\bicacls\b",
    r"\battrib\b",
    r"\bsetfacl\b",
    r"\btakeown\b",
]

# System Configuration & Service Management
SYSTEM_CONFIG_PATTERNS = [
    r"\bsystemctl\s+(enable|disable|start|stop|restart)\b",
    r"\bsc\s+config\b",
    r"\breg\s+(add|delete)\b",
    r"\bregedit\b",
    r"\bpowercfg\b",
    r"\bservices\.msc\b",
    r"\bupdate-rc\.d\b",
    r"\bchkconfig\b",
]

# Destructive or High-Risk Commands
DESTRUCTIVE_COMMAND_PATTERNS = [
    r"\brm\s+-rf\s+[^\s]*",           # Dangerous delete
    r"\bdel\s+/s\s+/q\b",             # Windows recursive delete
    r"\bmkfs\b",                      # Filesystem formatting
    r"\bformat\s+\w:",                # Windows format command
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bdd\s+if=.*of=.*",             # Disk cloning/dumping
    r"\bmv\s+/system\b",              # Moving system files
]

# Information Gathering Commands
INFO_COMMAND_PATTERNS = [
    r"\bcat\s+/etc/shadow\b",
    r"\bcat\s+/etc/passwd\b",
    r"\btype\s+.*\.(pem|key)\b",
    r"\bsudo\s+-l\b",
    r"\bwhoami\s+/priv\b",
]

# Network Administration Commands
NETWORK_COMMAND_PATTERNS = [
    r"\biptables\b",
    r"\broute\b",
    r"\bnetstat\b",
    r"\bifconfig\b",
    r"\bip\s+route\b",
    r"\bnetsh\b",
]