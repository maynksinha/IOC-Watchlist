import re
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse, urlunparse

from app.constants import IOCType


class InvalidIOCError(Exception):
    """Raised when a value cannot be classified as any known IOC type."""


_MD5_RE = re.compile(r"^[0-9a-fA-F]{32}$")
_SHA1_RE = re.compile(r"^[0-9a-fA-F]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_IPV4_RE = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")
_DOMAIN_RE = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")
_URL_SCHEME_RE = re.compile(r"^(https?|ftp)://", re.IGNORECASE)


# ── matchers ────────────────────────────────────────────────────────────────
def _is_hash(pattern: re.Pattern) -> Callable[[str], bool]:
    return lambda v: bool(pattern.match(v))


def _is_ipv4(v: str) -> bool:
    v = v.rstrip(".")
    m = _IPV4_RE.match(v)
    if not m:
        return False
    if not all(0 <= int(octet) <= 255 for octet in m.groups()):
        return False
    # Reject leading-zero octets (e.g. "01.02.03.04") — ambiguous / non-canonical.
    return all(part == "0" or not part.startswith("0") for part in v.split("."))


def _is_url(v: str) -> bool:
    if not _URL_SCHEME_RE.match(v):
        return False
    try:
        return bool(urlparse(v).netloc)
    except ValueError as exc:
        raise InvalidIOCError(f"Malformed URL: {v!r}") from exc


def _is_domain(v: str) -> bool:
    return bool(_DOMAIN_RE.match(v.rstrip(".")))


# ── canonicalizers ──────────────────────────────────────────────────────────
def _canon_lower(v: str) -> str:
    return v.lower()


def _canon_ipv4(v: str) -> str:
    return v.rstrip(".")


def _canon_domain(v: str) -> str:
    return v.rstrip(".").lower()


def _canon_url(v: str) -> str:
    try:
        parsed = urlparse(v)
    except ValueError as exc:
        raise InvalidIOCError(f"Malformed URL: {v!r}") from exc
    path = "" if parsed.path == "/" else parsed.path
    path = re.sub(r"%([0-9a-fA-F]{2})", lambda m: f"%{m.group(1).upper()}", path)
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.params, parsed.query, ""))


@dataclass(frozen=True)
class IOCDetector:
    type: IOCType
    matches: Callable[[str], bool]
    canonicalize: Callable[[str], str]


# Order matters: more specific types are checked first (hashes and IPv4 before
# the broad domain pattern). To support a new IOC type, add one entry here.
DETECTORS: tuple[IOCDetector, ...] = (
    IOCDetector(IOCType.MD5, _is_hash(_MD5_RE), _canon_lower),
    IOCDetector(IOCType.SHA1, _is_hash(_SHA1_RE), _canon_lower),
    IOCDetector(IOCType.SHA256, _is_hash(_SHA256_RE), _canon_lower),
    IOCDetector(IOCType.IPV4, _is_ipv4, _canon_ipv4),
    IOCDetector(IOCType.URL, _is_url, _canon_url),
    IOCDetector(IOCType.DOMAIN, _is_domain, _canon_domain),
)

_BY_TYPE: dict[IOCType, IOCDetector] = {d.type: d for d in DETECTORS}
