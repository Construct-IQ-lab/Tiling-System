/**
 * Calculator page functionality
 */

// Area form submission
document.getElementById('area-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const length = parseFloat(document.getElementById('length').value);
    const width = parseFloat(document.getElementById('width').value);
    const unit = document.getElementById('unit').value;
    
    try {
        const result = await api.calculateArea(length, width, unit);
        
        // Display result
        document.getElementById('area-value').textContent = 
            `${result.area} ${result.area_unit}`;
        document.getElementById('area-result').classList.remove('hidden');
        
        // Auto-fill material form
        document.getElementById('mat-area').value = result.area;
    } catch (error) {
        alert('Error calculating area: ' + error.message);
    }
});

// Materials form submission
document.getElementById('materials-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const area = parseFloat(document.getElementById('mat-area').value);
    const tileWidth = parseFloat(document.getElementById('tile-width').value);
    const tileHeight = parseFloat(document.getElementById('tile-height').value);
    const wastagePercent = parseFloat(document.getElementById('wastage').value);
    
    try {
        const result = await api.calculateMaterials({
            area,
            tile_width: tileWidth,
            tile_height: tileHeight,
            wastage_percent: wastagePercent,
            grout_width_mm: 3.0
        });
        
        const materials = result.results;
        
        // Display results
        document.getElementById('tiles-needed').textContent = materials.tiles_needed;
        document.getElementById('boxes-estimate').textContent = materials.boxes_estimate;
        document.getElementById('tiles-per-box').textContent = materials.tiles_per_box_estimate;
        document.getElementById('grout-needed').textContent = materials.grout_needed_kg;
        document.getElementById('grout-bags').textContent = materials.grout_bags;
        document.getElementById('adhesive-needed').textContent = materials.adhesive_needed_kg;
        document.getElementById('adhesive-bags').textContent = materials.adhesive_bags;
        document.getElementById('materials-result').classList.remove('hidden');
        
        // Auto-fill cost form
        document.getElementById('cost-tiles').value = materials.tiles_needed;
        document.getElementById('cost-grout-bags').value = materials.grout_bags;
        document.getElementById('cost-adhesive-bags').value = materials.adhesive_bags;
    } catch (error) {
        alert('Error calculating materials: ' + error.message);
    }
});

// Cost form submission
document.getElementById('cost-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const tilesNeeded = parseInt(document.getElementById('cost-tiles').value);
    const tilePrice = parseFloat(document.getElementById('tile-price').value);
    const groutBags = parseInt(document.getElementById('cost-grout-bags').value);
    const groutPrice = parseFloat(document.getElementById('grout-price').value);
    const adhesiveBags = parseInt(document.getElementById('cost-adhesive-bags').value);
    const adhesivePrice = parseFloat(document.getElementById('adhesive-price').value);
    const laborCost = parseFloat(document.getElementById('labor-cost').value);
    
    try {
        const result = await api.calculateCost({
            tiles_needed: tilesNeeded,
            tile_price: tilePrice,
            grout_bags: groutBags,
            grout_price: groutPrice,
            adhesive_bags: adhesiveBags,
            adhesive_price: adhesivePrice,
            labor_cost: laborCost
        });
        
        const cost = result.results;
        
        // Display results
        document.getElementById('tiles-cost').textContent = cost.tiles_cost.toFixed(2);
        document.getElementById('grout-cost').textContent = cost.grout_cost.toFixed(2);
        document.getElementById('adhesive-cost').textContent = cost.adhesive_cost.toFixed(2);
        document.getElementById('labor-cost-result').textContent = cost.labor_cost.toFixed(2);
        document.getElementById('materials-cost').textContent = cost.materials_cost.toFixed(2);
        document.getElementById('total-cost').textContent = cost.total_cost.toFixed(2);
        document.getElementById('cost-result').classList.remove('hidden');
    } catch (error) {
        alert('Error calculating cost: ' + error.message);
    }
});
