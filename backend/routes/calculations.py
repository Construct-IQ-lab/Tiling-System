from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from services.calculator import TilingCalculator


# Pydantic Schemas
class AreaCalculation(BaseModel):
    """Schema for area calculation request"""
    length: float = Field(..., gt=0, description="Length in specified unit")
    width: float = Field(..., gt=0, description="Width in specified unit")
    unit: str = Field(default="meters", description="Unit of measurement")


class MaterialCalculation(BaseModel):
    """Schema for material calculation request"""
    area: float = Field(..., gt=0, description="Area in square meters")
    tile_width: float = Field(..., gt=0, description="Tile width in centimeters")
    tile_height: float = Field(..., gt=0, description="Tile height in centimeters")
    wastage_percent: float = Field(default=10.0, ge=0, le=100, description="Wastage percentage")
    grout_width_mm: float = Field(default=3.0, gt=0, description="Grout joint width in millimeters")


class CostCalculation(BaseModel):
    """Schema for cost calculation request"""
    tiles_needed: int = Field(..., gt=0, description="Number of tiles needed")
    tile_price: float = Field(..., ge=0, description="Price per tile")
    grout_bags: int = Field(..., ge=0, description="Number of grout bags")
    grout_price: float = Field(..., ge=0, description="Price per grout bag")
    adhesive_bags: int = Field(..., ge=0, description="Number of adhesive bags")
    adhesive_price: float = Field(..., ge=0, description="Price per adhesive bag")
    labor_cost: float = Field(default=0.0, ge=0, description="Labor cost")


# Router
router = APIRouter()
calculator = TilingCalculator()


@router.post("/area")
def calculate_area(data: AreaCalculation):
    """
    Calculate area from length and width
    
    Returns area in square units
    """
    area = calculator.calculate_area(data.length, data.width)
    return {
        "length": data.length,
        "width": data.width,
        "unit": data.unit,
        "area": area,
        "area_unit": f"square {data.unit}"
    }


@router.post("/materials")
def calculate_materials(data: MaterialCalculation):
    """
    Calculate materials needed for tiling project
    
    Returns tiles, grout, and adhesive requirements
    """
    materials = calculator.calculate_materials(
        area=data.area,
        tile_width=data.tile_width,
        tile_height=data.tile_height,
        wastage_percent=data.wastage_percent,
        grout_width_mm=data.grout_width_mm
    )
    
    return {
        "input": {
            "area": data.area,
            "tile_dimensions": {
                "width_cm": data.tile_width,
                "height_cm": data.tile_height
            },
            "wastage_percent": data.wastage_percent,
            "grout_width_mm": data.grout_width_mm
        },
        "results": materials
    }


@router.post("/cost")
def calculate_cost(data: CostCalculation):
    """
    Calculate total project cost with breakdown
    
    Returns detailed cost breakdown
    """
    cost = calculator.calculate_cost(
        tiles_needed=data.tiles_needed,
        tile_price=data.tile_price,
        grout_bags=data.grout_bags,
        grout_price=data.grout_price,
        adhesive_bags=data.adhesive_bags,
        adhesive_price=data.adhesive_price,
        labor_cost=data.labor_cost
    )
    
    return {
        "input": {
            "tiles_needed": data.tiles_needed,
            "tile_price": data.tile_price,
            "grout_bags": data.grout_bags,
            "grout_price": data.grout_price,
            "adhesive_bags": data.adhesive_bags,
            "adhesive_price": data.adhesive_price,
            "labor_cost": data.labor_cost
        },
        "results": cost
    }
