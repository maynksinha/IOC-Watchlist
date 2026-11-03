from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared limiter keyed by client IP. Apply to routes with @limiter.limit(...).
limiter = Limiter(key_func=get_remote_address)
