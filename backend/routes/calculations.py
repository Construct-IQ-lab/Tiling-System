from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class AreaCalculationRequest(BaseModel):
    length: float
    width: float
    unit: str = "meters"


class AreaCalculationResponse(BaseModel):
    area: float
    unit: str


class MaterialCalculationRequest(BaseModel):
    area: float
    tile_length: float
    tile_width: float
    wastage_percent: float = 10.0
    grout_joint_width: float = 3.0  # mm


class MaterialCalculationResponse(BaseModel):
    tiles_needed: int
    grout_kg: float
    adhesive_bags: int
    total_cost: Optional[float] = None


class CostCalculationRequest(BaseModel):
    tiles_needed: int
    tile_price: float
    grout_kg: float
    grout_price_per_kg: float
    adhesive_bags: int
    adhesive_price_per_bag: float
    labor_cost: Optional[float] = 0.0


class CostCalculationResponse(BaseModel):
    tiles_cost: float
    grout_cost: float
    adhesive_cost: float
    labor_cost: float
    total_cost: float


@router.post("/area", response_model=AreaCalculationResponse)
async def calculate_area(request: AreaCalculationRequest):
    """Calculate area based on dimensions"""
    area = request.length * request.width
    return AreaCalculationResponse(
        area=round(area, 2),
        unit=f"square {request.unit}"
    )


@router.post("/materials", response_model=MaterialCalculationResponse)
async def calculate_materials(request: MaterialCalculationRequest):
    """Calculate material requirements for tiling project"""
    # Calculate adjusted area with wastage
    adjusted_area = request.area * (1 + request.wastage_percent / 100)
    
    # Calculate tile quantity
    tile_area = request.tile_length * request.tile_width
    tiles_needed = int(adjusted_area / tile_area) + 1
    
    # Calculate grout (simplified: ~1kg per 10 sqm for 3mm joints)
    grout_kg = round((request.area / 10) * (request.grout_joint_width / 3), 2)
    
    # Calculate adhesive (simplified: 1 bag per 5 sqm)
    adhesive_bags = int(adjusted_area / 5) + 1
    
    return MaterialCalculationResponse(
        tiles_needed=tiles_needed,
        grout_kg=grout_kg,
        adhesive_bags=adhesive_bags
    )


@router.post("/cost", response_model=CostCalculationResponse)
async def calculate_cost(request: CostCalculationRequest):
    """Calculate total project cost"""
    tiles_cost = request.tiles_needed * request.tile_price
    grout_cost = request.grout_kg * request.grout_price_per_kg
    adhesive_cost = request.adhesive_bags * request.adhesive_price_per_bag
    labor_cost = request.labor_cost or 0.0
    
    total_cost = tiles_cost + grout_cost + adhesive_cost + labor_cost
    
    return CostCalculationResponse(
        tiles_cost=round(tiles_cost, 2),
        grout_cost=round(grout_cost, 2),
        adhesive_cost=round(adhesive_cost, 2),
        labor_cost=round(labor_cost, 2),
        total_cost=round(total_cost, 2)
    )
