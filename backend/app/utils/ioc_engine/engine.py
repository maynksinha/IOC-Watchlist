import re
from urllib.parse import urlparse, urlunparse

from app.constants import IOCType


class InvalidIOCError(Exception):
    pass


_DEFANG_PATTERNS = [
    (re.compile(r'hxxps://', re.IGNORECASE), 'https://'),
    (re.compile(r'hxxp://', re.IGNORECASE), 'http://'),
    (re.compile(r'http\[s\]://', re.IGNORECASE), 'https://'),
    (re.compile(r'http\[:\]//', re.IGNORECASE), 'http://'),
    (re.compile(r'\[\.\]|\(\.\)|\{\.\}'), '.'),
    (re.compile(r'\[dot\]|\(dot\)|\{dot\}', re.IGNORECASE), '.'),
    (re.compile(r'\[:\]|\(:\)'), ':'),
    (re.compile(r'\[/\]'), '/'),
    (re.compile(r'\[@\]'), '@'),
]

_MD5_RE = re.compile(r'^[0-9a-fA-F]{32}$')
_SHA1_RE = re.compile(r'^[0-9a-fA-F]{40}$')
_SHA256_RE = re.compile(r'^[0-9a-fA-F]{64}$')
_IPV4_RE = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
_DOMAIN_RE = re.compile(r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')


def defang(raw: str) -> str:
    result = raw.strip()
    for pattern, replacement in _DEFANG_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


def detect_type(value: str) -> IOCType:
    v = value.strip()

    if _MD5_RE.match(v):
        return IOCType.MD5
    if _SHA1_RE.match(v):
        return IOCType.SHA1
    if _SHA256_RE.match(v):
        return IOCType.SHA256

    m = _IPV4_RE.match(v.rstrip('.'))
    if m:
        octets = [int(m.group(i)) for i in range(1, 5)]
        if all(0 <= o <= 255 for o in octets):
            parts = v.rstrip('.').split('.')
            if all(not p.startswith('0') or p == '0' for p in parts):
                return IOCType.IPV4

    if re.match(r'^(https?|ftp)://', v, re.IGNORECASE):
        try:
                parsed = urlparse(v)
                if parsed.netloc:
                        return IOCType.URL
        except ValueError as exc:
            raise InvalidIOCError(f"Malformed URL: {v!r}") from exc

    clean = v.rstrip('.')
    if _DOMAIN_RE.match(clean):
        return IOCType.DOMAIN

    raise InvalidIOCError(f"Cannot determine IOC type for: {v!r}")


def canonicalize(defanged: str, ioc_type: IOCType) -> str:
    v = defanged.strip()

    if ioc_type in (IOCType.MD5, IOCType.SHA1, IOCType.SHA256):
        return v.lower()

    if ioc_type == IOCType.IPV4:
        return v.rstrip('.')

    if ioc_type == IOCType.DOMAIN:
        return v.rstrip('.').lower()

    if ioc_type == IOCType.URL:
        try:
             parsed = urlparse(v)
        except ValueError as exc:
            raise InvalidIOCError(f"Malformed URL during canonicalize: {v!r}") from exc
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        path = parsed.path
        if path == '/':
            path = ''
        path = re.sub(r'%([0-9a-fA-F]{2})', lambda m: f'%{m.group(1).upper()}', path)
        canonical = urlunparse((scheme, netloc, path, parsed.params, parsed.query, ''))
        return canonical

    raise InvalidIOCError(f"Unknown ioc_type: {ioc_type}")


def normalize_and_detect(raw: str) -> tuple[str, IOCType]:
    defanged = defang(raw)
    ioc_type = detect_type(defanged)
    canonical = canonicalize(defanged, ioc_type)
    return canonical, ioc_type
