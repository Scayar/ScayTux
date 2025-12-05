"""
TUX Droid AI Control - Health Check Routes
==========================================

Health and status endpoints for the API.
"""

from fastapi import APIRouter, Depends
from ..schemas.tux_schemas import HealthResponse, TuxStatus

router = APIRouter(tags=["Health"])


def get_tux_controller():
    """Dependency to get the TUX controller instance."""
    from ..main import tux_controller
    return tux_controller


def get_settings():
    """Dependency to get settings."""
    from config.settings import settings
    return settings


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check API health and TUX connection status"
)
async def health_check(
    controller=Depends(get_tux_controller),
    settings=Depends(get_settings)
):
    """
    Perform a health check on the API.
    
    Returns:
        HealthResponse: Current health status
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        tux_connected=controller.is_connected() if controller else False,
        mode=settings.tux_mode
    )


@router.get(
    "/status",
    response_model=TuxStatus,
    summary="TUX Status",
    description="Get detailed TUX Droid status information"
)
async def get_status(controller=Depends(get_tux_controller)):
    """
    Get detailed TUX Droid status.
    
    Returns:
        TuxStatus: Current TUX status and state
    """
    if controller is None:
        return TuxStatus(
            connected=False,
            driver_type="none",
            device_path=None,
            simulated_state=None,
            last_action=None,
            actions_executed=None
        )
    
    status = controller.get_status()
    return TuxStatus(
        connected=status.get("connected", False),
        driver_type=status.get("driver_type", "unknown"),
        device_path=status.get("device_path"),
        simulated_state=status.get("simulated_state"),
        last_action=status.get("last_action"),
        actions_executed=status.get("actions_executed")
    )

