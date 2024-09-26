# circuit_breaker.py
from pybreaker import CircuitBreaker


def setup_circuit_breaker() -> CircuitBreaker:
    return CircuitBreaker(fail_max=3, reset_timeout=60)
