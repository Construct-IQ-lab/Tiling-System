// Tiling Calculator Logic

let calculatorStep = 1;
let calculationData = {};

/**
 * Initialize calculator
 */
function initCalculator() {
    calculatorStep = 1;
    calculationData = {};
    showStep(1);
}

/**
 * Show specific calculator step
 * @param {number} step - Step number to show
 */
function showStep(step) {
    calculatorStep = step;
    
    // Hide all forms
    document.querySelectorAll('.calculator-form').forEach(form => {
        form.style.display = 'none';
    });
    
    // Show current form
    const currentForm = document.getElementById(`step-${step}-form`);
    if (currentForm) {
        currentForm.style.display = 'block';
    }
    
    // Update step indicators
    document.querySelectorAll('.calculator-step').forEach((stepEl, index) => {
        stepEl.classList.remove('active', 'completed');
        if (index + 1 < step) {
            stepEl.classList.add('completed');
        } else if (index + 1 === step) {
            stepEl.classList.add('active');
        }
    });
    
    // Hide/show results
    const resultsSection = document.getElementById('calculator-results');
    if (resultsSection) {
        resultsSection.style.display = step === 4 ? 'block' : 'none';
    }
}

/**
 * Handle area calculation form submission
 */
async function handleAreaCalculation(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    const data = {
        length: parseFloat(form.length.value),
        width: parseFloat(form.width.value)
    };
    
    setButtonLoading(submitButton, true);
    
    try {
        const result = await apiRequest('/calculations/area', 'POST', data, true);
        
        // Store result
        calculationData.area = result.area;
        calculationData.length = data.length;
        calculationData.width = data.width;
        
        // Pre-fill next form
        const materialsForm = document.getElementById('step-2-form');
        if (materialsForm) {
            materialsForm.area.value = result.area;
        }
        
        showSuccess(`Area calculated: ${result.area} m²`);
        showStep(2);
        
    } catch (error) {
        console.error('Error calculating area:', error);
        showError(error.message || 'Failed to calculate area');
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * Handle materials calculation form submission
 */
async function handleMaterialsCalculation(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    const data = {
        area: parseFloat(form.area.value),
        tile_length: parseFloat(form.tile_length.value),
        tile_width: parseFloat(form.tile_width.value),
        grout_joint_width: parseFloat(form.grout_joint_width.value),
        wastage_percent: parseFloat(form.wastage_percent.value)
    };
    
    setButtonLoading(submitButton, true);
    
    try {
        const result = await apiRequest('/calculations/materials', 'POST', data, true);
        
        // Store result
        calculationData.materials = result;
        
        // Pre-fill cost calculation form
        const costForm = document.getElementById('step-3-form');
        if (costForm) {
            costForm.tiles_needed.value = result.tiles_needed;
            costForm.grout_needed.value = result.grout_needed;
            costForm.adhesive_needed.value = result.adhesive_needed;
        }
        
        showSuccess('Materials calculated successfully');
        showStep(3);
        
    } catch (error) {
        console.error('Error calculating materials:', error);
        showError(error.message || 'Failed to calculate materials');
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * Handle cost calculation form submission
 */
async function handleCostCalculation(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    
    const data = {
        tiles_needed: parseFloat(form.tiles_needed.value),
        tile_price: parseFloat(form.tile_price.value),
        grout_needed: parseFloat(form.grout_needed.value),
        grout_price: parseFloat(form.grout_price.value),
        adhesive_needed: parseFloat(form.adhesive_needed.value),
        adhesive_price: parseFloat(form.adhesive_price.value),
        labor_hours: parseFloat(form.labor_hours.value || 0),
        labor_rate: parseFloat(form.labor_rate.value || 0)
    };
    
    setButtonLoading(submitButton, true);
    
    try {
        const result = await apiRequest('/calculations/cost', 'POST', data, true);
        
        // Store result
        calculationData.cost = result;
        
        // Display results
        displayCalculationResults();
        showStep(4);
        
    } catch (error) {
        console.error('Error calculating cost:', error);
        showError(error.message || 'Failed to calculate cost');
    } finally {
        setButtonLoading(submitButton, false);
    }
}

/**
 * Display calculation results
 */
function displayCalculationResults() {
    const resultsGrid = document.getElementById('results-grid');
    if (!resultsGrid) return;
    
    const materials = calculationData.materials || {};
    const cost = calculationData.cost || {};
    
    resultsGrid.innerHTML = `
        <div class="result-card">
            <div class="result-label">Total Area</div>
            <div class="result-value">${calculationData.area || 0}<span class="result-unit">m²</span></div>
        </div>
        
        <div class="result-card">
            <div class="result-label">Tiles Needed</div>
            <div class="result-value">${materials.tiles_needed || 0}<span class="result-unit">pcs</span></div>
        </div>
        
        <div class="result-card">
            <div class="result-label">Grout Needed</div>
            <div class="result-value">${materials.grout_needed || 0}<span class="result-unit">kg</span></div>
        </div>
        
        <div class="result-card">
            <div class="result-label">Adhesive Needed</div>
            <div class="result-value">${materials.adhesive_needed || 0}<span class="result-unit">kg</span></div>
        </div>
        
        <div class="result-card highlight">
            <div class="result-label">Total Cost</div>
            <div class="result-value">${formatCurrency(cost.total_cost || 0)}</div>
        </div>
    `;
}

/**
 * Reset calculator
 */
function resetCalculator() {
    initCalculator();
    document.querySelectorAll('.calculator-form').forEach(form => {
        form.reset();
    });
}

/**
 * Save calculation (placeholder)
 */
function saveCalculation() {
    showError('Save calculation functionality coming soon');
}

/**
 * Initialize calculator on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname.includes('calculator.html')) {
        initCalculator();
        
        // Setup form submissions
        const areaForm = document.getElementById('step-1-form');
        if (areaForm) {
            areaForm.addEventListener('submit', handleAreaCalculation);
        }
        
        const materialsForm = document.getElementById('step-2-form');
        if (materialsForm) {
            materialsForm.addEventListener('submit', handleMaterialsCalculation);
        }
        
        const costForm = document.getElementById('step-3-form');
        if (costForm) {
            costForm.addEventListener('submit', handleCostCalculation);
        }
    }
});
