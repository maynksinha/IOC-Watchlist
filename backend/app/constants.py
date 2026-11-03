from enum import Enum


class IOCType(str, Enum):
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    IPV4 = "ipv4"
    DOMAIN = "domain"
    URL = "url"


class TableName(str, Enum):
    IOC = "ioc"
    TAG = "tag"
    IOC_TAG = "ioc_tag"


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
    INTERNAL_ERROR = "INTERNAL_ERROR"


class DBDefault(str, Enum):
    SQLITE_URL = "sqlite+aiosqlite:///./data/ioc_watchlist.db"


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
