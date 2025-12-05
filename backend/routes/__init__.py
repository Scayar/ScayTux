"""
TUX Droid AI Control - API Routes Package
"""

from .tux_routes import router as tux_router
from .health import router as health_router

__all__ = ["tux_router", "health_router"]

