"""
TUX Droid AI Control - Backend API Server
=========================================

FastAPI-based REST API server for controlling TUX Droid.

Usage:
    # Development
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    
    # Production
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
"""

import sys
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings
from backend.routes import tux_router, health_router
from tux.controller import TuxController
from tux.driver import TuxDriver
from stubs.mock_driver import MockTuxDriver

# ==========================================
# Logging Configuration
# ==========================================

def setup_logging():
    """Configure logging for the application."""
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

setup_logging()
logger = logging.getLogger(__name__)

# ==========================================
# Global TUX Controller
# ==========================================

tux_controller: TuxController = None


def initialize_tux_controller() -> TuxController:
    """
    Initialize the TUX controller with appropriate driver.
    
    Uses MockTuxDriver in DEV mode, TuxDriver in PROD mode.
    """
    global tux_controller
    
    if settings.is_dev_mode:
        logger.info("🐧 Initializing TUX controller in DEV mode (mock driver)")
        driver = MockTuxDriver(simulate_delay=True, delay_ms=50)
    else:
        logger.info(f"🐧 Initializing TUX controller in PROD mode (device: {settings.tux_device_path})")
        driver = TuxDriver(device_path=settings.tux_device_path)
    
    tux_controller = TuxController(driver)
    
    # Auto-connect in DEV mode
    if settings.is_dev_mode:
        tux_controller.connect()
    
    return tux_controller


# ==========================================
# Application Lifecycle
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("=" * 50)
    logger.info("🚀 TUX Droid AI Control API Starting...")
    logger.info(f"   Mode: {settings.tux_mode}")
    logger.info(f"   Host: {settings.api_host}:{settings.api_port}")
    logger.info("=" * 50)
    
    initialize_tux_controller()
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down TUX Droid AI Control API...")
    if tux_controller and tux_controller.is_connected():
        tux_controller.disconnect()
    logger.info("👋 Goodbye!")


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="TUX Droid AI Control API",
    description="""
    ## 🐧 TUX Droid AI Control System
    
    REST API for controlling TUX Droid via HTTP requests.
    
    ### Features:
    - **Eyes**: Blink, open, close
    - **Mouth**: Move, open, close
    - **Wings**: Wave, raise, lower
    - **Spin**: Rotate left/right
    - **LEDs**: On, off, toggle, pulse
    - **Sound**: Play sounds, mute/unmute
    - **Sleep**: Sleep and wake modes
    
    ### Modes:
    - **DEV**: Uses mock driver for testing without hardware
    - **PROD**: Uses real hardware driver
    
    ### Authentication:
    Currently no authentication required (local network use).
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ==========================================
# CORS Middleware
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Exception Handlers
# ==========================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "internal_error",
            "message": str(exc),
            "details": None
        }
    )

# ==========================================
# Include Routers
# ==========================================

app.include_router(health_router)
app.include_router(tux_router)

# ==========================================
# Root Endpoint
# ==========================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "TUX Droid AI Control API",
        "version": "1.0.0",
        "mode": settings.tux_mode,
        "docs": "/docs",
        "health": "/health",
        "status": "/status"
    }


# ==========================================
# Main Entry Point
# ==========================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.is_dev_mode,
        log_level=settings.log_level.lower()
    )

