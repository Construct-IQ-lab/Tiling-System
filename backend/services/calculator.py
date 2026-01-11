import math


class TilingCalculator:
    """Service class for tiling calculations"""
    
    @staticmethod
    def calculate_area(length: float, width: float) -> float:
        """
        Calculate area from length and width
        
        Args:
            length: Length in specified unit
            width: Width in specified unit
            
        Returns:
            Area rounded to 2 decimal places
        """
        area = length * width
        return round(area, 2)
    
    @staticmethod
    def calculate_materials(
        area: float,
        tile_width: float,
        tile_height: float,
        wastage_percent: float = 10.0,
        grout_width_mm: float = 3.0
    ) -> dict:
        """
        Calculate materials needed for tiling
        
        Args:
            area: Total area in square meters
            tile_width: Tile width in centimeters
            tile_height: Tile height in centimeters
            wastage_percent: Percentage of wastage (default 10%)
            grout_width_mm: Grout joint width in millimeters (default 3mm)
            
        Returns:
            Dictionary with material calculations
        """
        # Convert tile dimensions from cm to m
        tile_width_m = tile_width / 100
        tile_height_m = tile_height / 100
        
        # Calculate tile area in square meters
        tile_area = tile_width_m * tile_height_m
        
        # Calculate base tiles needed
        base_tiles = area / tile_area
        
        # Add wastage
        wastage_multiplier = 1 + (wastage_percent / 100)
        tiles_with_wastage = base_tiles * wastage_multiplier
        tiles_needed = math.ceil(tiles_with_wastage)
        
        # Calculate grout needed (approximately 1 kg per 4 m²)
        grout_kg = area / 4
        grout_bags = math.ceil(grout_kg / 5)  # Assuming 5kg bags
        
        # Calculate adhesive needed (approximately 5 kg per m²)
        adhesive_kg = area * 5
        adhesive_bags = math.ceil(adhesive_kg / 25)  # Assuming 25kg bags
        
        # Estimate boxes (assuming 10 tiles per box as average)
        tiles_per_box = 10
        boxes_needed = math.ceil(tiles_needed / tiles_per_box)
        
        return {
            "area": round(area, 2),
            "tile_area": round(tile_area, 4),
            "tiles_needed": tiles_needed,
            "tiles_with_wastage": round(tiles_with_wastage, 2),
            "wastage_percent": wastage_percent,
            "boxes_estimate": boxes_needed,
            "tiles_per_box_estimate": tiles_per_box,
            "grout_needed_kg": round(grout_kg, 2),
            "grout_bags": grout_bags,
            "adhesive_needed_kg": round(adhesive_kg, 2),
            "adhesive_bags": adhesive_bags
        }
    
    @staticmethod
    def calculate_cost(
        tiles_needed: int,
        tile_price: float,
        grout_bags: int,
        grout_price: float,
        adhesive_bags: int,
        adhesive_price: float,
        labor_cost: float = 0.0
    ) -> dict:
        """
        Calculate total project cost
        
        Args:
            tiles_needed: Number of tiles needed
            tile_price: Price per tile
            grout_bags: Number of grout bags
            grout_price: Price per grout bag
            adhesive_bags: Number of adhesive bags
            adhesive_price: Price per adhesive bag
            labor_cost: Labor cost (default 0)
            
        Returns:
            Dictionary with cost breakdown
        """
        tiles_cost = tiles_needed * tile_price
        grout_cost = grout_bags * grout_price
        adhesive_cost = adhesive_bags * adhesive_price
        materials_cost = tiles_cost + grout_cost + adhesive_cost
        total_cost = materials_cost + labor_cost
        
        return {
            "tiles_cost": round(tiles_cost, 2),
            "grout_cost": round(grout_cost, 2),
            "adhesive_cost": round(adhesive_cost, 2),
            "materials_cost": round(materials_cost, 2),
            "labor_cost": round(labor_cost, 2),
            "total_cost": round(total_cost, 2),
            "breakdown": {
                "tiles": {
                    "quantity": tiles_needed,
                    "unit_price": tile_price,
                    "total": round(tiles_cost, 2)
                },
                "grout": {
                    "bags": grout_bags,
                    "unit_price": grout_price,
                    "total": round(grout_cost, 2)
                },
                "adhesive": {
                    "bags": adhesive_bags,
                    "unit_price": adhesive_price,
                    "total": round(adhesive_cost, 2)
                },
                "labor": round(labor_cost, 2)
            }
        }
