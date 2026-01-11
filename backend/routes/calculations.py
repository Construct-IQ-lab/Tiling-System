from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from services.calculator import TilingCalculator

router = APIRouter(prefix="/calculations", tags=["Calculations"])


class TileQuantityRequest(BaseModel):
    room_length: float = Field(..., gt=0, description="Length of the room")
    room_width: float = Field(..., gt=0, description="Width of the room")
    tile_length: float = Field(..., gt=0, description="Length of one tile")
    tile_width: float = Field(..., gt=0, description="Width of one tile")
    wastage_percentage: float = Field(10.0, ge=0, le=100, description="Wastage percentage")


class CostRequest(BaseModel):
    tiles_needed: int = Field(..., gt=0, description="Number of tiles required")
    price_per_tile: float = Field(..., gt=0, description="Price per tile")
    labor_cost: Optional[float] = Field(None, ge=0, description="Labor cost")
    additional_materials_cost: Optional[float] = Field(None, ge=0, description="Additional materials cost")


class ProjectCalculationRequest(BaseModel):
    room_length: float = Field(..., gt=0)
    room_width: float = Field(..., gt=0)
    tile_length: float = Field(..., gt=0)
    tile_width: float = Field(..., gt=0)
    price_per_tile: float = Field(..., gt=0)
    wastage_percentage: float = Field(10.0, ge=0, le=100)
    labor_cost: Optional[float] = Field(None, ge=0)
    additional_materials_cost: Optional[float] = Field(None, ge=0)


@router.post("/tile-quantity")
async def calculate_tile_quantity(request: TileQuantityRequest):
    """
    Calculate the number of tiles needed for a room.
    
    Args:
        request: Room and tile dimensions with wastage percentage
        
    Returns:
        Calculation results including total tiles needed
    """
    try:
        result = TilingCalculator.calculate_tile_quantity(
            room_length=request.room_length,
            room_width=request.room_width,
            tile_length=request.tile_length,
            tile_width=request.tile_width,
            wastage_percentage=request.wastage_percentage
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cost")
async def calculate_cost(request: CostRequest):
    """
    Calculate the total cost for a tiling project.
    
    Args:
        request: Cost parameters including tiles, labor, and materials
        
    Returns:
        Cost breakdown
    """
    try:
        result = TilingCalculator.calculate_cost(
            tiles_needed=request.tiles_needed,
            price_per_tile=request.price_per_tile,
            labor_cost=request.labor_cost,
            additional_materials_cost=request.additional_materials_cost
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/project")
async def calculate_project(request: ProjectCalculationRequest):
    """
    Complete project calculation including tiles and costs.
    
    Args:
        request: Complete project parameters
        
    Returns:
        Full project calculation with quantities and costs
    """
    try:
        result = TilingCalculator.calculate_project(
            room_length=request.room_length,
            room_width=request.room_width,
            tile_length=request.tile_length,
            tile_width=request.tile_width,
            price_per_tile=request.price_per_tile,
            wastage_percentage=request.wastage_percentage,
            labor_cost=request.labor_cost,
            additional_materials_cost=request.additional_materials_cost
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
