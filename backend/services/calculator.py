from typing import Dict, Optional
from decimal import Decimal


class TilingCalculator:
    """
    Service class for tiling calculations.
    Handles tile quantity, cost, and area calculations.
    """

    @staticmethod
    def calculate_tile_quantity(
        room_length: float,
        room_width: float,
        tile_length: float,
        tile_width: float,
        wastage_percentage: float = 10.0
    ) -> Dict[str, float]:
        """
        Calculate the number of tiles needed for a room.
        
        Args:
            room_length: Length of the room in meters/feet
            room_width: Width of the room in meters/feet
            tile_length: Length of one tile in meters/feet
            tile_width: Width of one tile in meters/feet
            wastage_percentage: Percentage of extra tiles for wastage (default 10%)
            
        Returns:
            Dictionary containing calculation results
        """
        # Calculate areas
        room_area = room_length * room_width
        tile_area = tile_length * tile_width
        
        # Calculate base tile quantity
        base_tiles_needed = room_area / tile_area
        
        # Add wastage
        wastage_multiplier = 1 + (wastage_percentage / 100)
        total_tiles_needed = base_tiles_needed * wastage_multiplier
        
        # Round up to nearest whole tile
        total_tiles_needed = int(total_tiles_needed) + (1 if total_tiles_needed % 1 > 0 else 0)
        
        return {
            "room_area": round(room_area, 2),
            "tile_area": round(tile_area, 4),
            "base_tiles_needed": round(base_tiles_needed, 2),
            "wastage_tiles": round(total_tiles_needed - base_tiles_needed, 2),
            "total_tiles_needed": total_tiles_needed,
            "wastage_percentage": wastage_percentage
        }

    @staticmethod
    def calculate_cost(
        tiles_needed: int,
        price_per_tile: float,
        labor_cost: Optional[float] = None,
        additional_materials_cost: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Calculate the total cost for a tiling project.
        
        Args:
            tiles_needed: Number of tiles required
            price_per_tile: Price per individual tile
            labor_cost: Optional labor cost
            additional_materials_cost: Optional cost for grout, adhesive, etc.
            
        Returns:
            Dictionary containing cost breakdown
        """
        tiles_cost = tiles_needed * price_per_tile
        labor = labor_cost or 0
        materials = additional_materials_cost or 0
        
        total_cost = tiles_cost + labor + materials
        
        return {
            "tiles_cost": round(tiles_cost, 2),
            "labor_cost": round(labor, 2),
            "materials_cost": round(materials, 2),
            "total_cost": round(total_cost, 2)
        }

    @staticmethod
    def calculate_project(
        room_length: float,
        room_width: float,
        tile_length: float,
        tile_width: float,
        price_per_tile: float,
        wastage_percentage: float = 10.0,
        labor_cost: Optional[float] = None,
        additional_materials_cost: Optional[float] = None
    ) -> Dict:
        """
        Complete project calculation including tiles and costs.
        
        Returns:
            Dictionary with complete project calculations
        """
        quantity_calc = TilingCalculator.calculate_tile_quantity(
            room_length, room_width, tile_length, tile_width, wastage_percentage
        )
        
        cost_calc = TilingCalculator.calculate_cost(
            quantity_calc["total_tiles_needed"],
            price_per_tile,
            labor_cost,
            additional_materials_cost
        )
        
        return {
            "quantities": quantity_calc,
            "costs": cost_calc
        }
