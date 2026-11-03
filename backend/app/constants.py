from enum import Enum


class IOCType(str, Enum):
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    IPV4 = "ipv4"
    DOMAIN = "domain"
    URL = "url"


class APIPrefix(str, Enum):
    IOCS = "/api/v1/iocs"
    TAGS = "/api/v1/tags"


class APITag(str, Enum):
    IOCS = "iocs"
    TAGS = "tags"
    HEALTH = "health"


class ErrorCode(str, Enum):
    INVALID_IOC = "INVALID_IOC"
    DUPLICATE_IOC = "DUPLICATE_IOC"
    NOT_FOUND = "NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RATE_LIMITED = "RATE_LIMITED"
    PAYLOAD_TOO_LARGE = "PAYLOAD_TOO_LARGE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class AppDefault(str, Enum):
    TITLE = "IOC Watchlist API"
    VERSION = "1.0.0"
    DESCRIPTION = "Indicator of Compromise watchlist — ingest, normalize, tag, and query IOCs."
    CORS_ORIGINS = "http://localhost:5173"


class Env(str, Enum):
    DEV = "development"
    PROD = "production"


class EnvFilePath(str, Enum):
    ENV = ".env"
    DEFAULT = ".env.example"


PAGINATION_DEFAULT_PAGE = 1
PAGINATION_DEFAULT_SIZE = 50
PAGINATION_MAX_SIZE = 200

# Input validation caps — keep in sync with frontend/src/constants.js
MAX_VALUE_LENGTH = 2048
MAX_NOTE_LENGTH = 1000
MAX_TAGS = 20
MAX_TAG_LENGTH = 50
MAX_BODY_BYTES = 64 * 1024  # reject request bodies larger than 64 KB

# Rate limiting (per client IP) applied to write endpoints
RATE_LIMIT_WRITE = "30/minute"
