from app.constants import IOCType

from .defang import defang
from .detectors import DETECTORS, _BY_TYPE, InvalidIOCError


def detect_type(value: str) -> IOCType:
    """Classify an already-defanged value. Raises InvalidIOCError if unknown."""
    v = value.strip()
    for detector in DETECTORS:
        if detector.matches(v):
            return detector.type
    raise InvalidIOCError(f"Cannot determine IOC type for: {v!r}")


def normalize_and_detect(raw: str) -> tuple[str, IOCType]:
    """Defang, classify, and canonicalize a raw IOC in one step."""
    defanged = defang(raw)
    ioc_type = detect_type(defanged)
    canonical = _BY_TYPE[ioc_type].canonicalize(defanged.strip())
    return canonical, ioc_type
