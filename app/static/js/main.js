/**
 * UTH Student Nutrition Meal Planner - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    // === 1. THEME TOGGLE (LIGHT / DARK MODE) ===
    const themeToggleBtn = document.getElementById('theme-toggle');
    const bodyEl = document.body;

    // Load saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light-mode';
    bodyEl.className = savedTheme;
    updateThemeToggleIcon(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function () {
            const currentTheme = bodyEl.className;
            let newTheme = 'light-mode';
            
            if (currentTheme === 'light-mode') {
                newTheme = 'dark-mode';
            }
            
            bodyEl.className = newTheme;
            localStorage.setItem('theme', newTheme);
            updateThemeToggleIcon(newTheme);
            showToast(newTheme === 'dark-mode' ? "Đã bật giao diện Tối" : "Đã bật giao diện Sáng", "success");
        });
    }

    function updateThemeToggleIcon(theme) {
        if (!themeToggleBtn) return;
        const icon = themeToggleBtn.querySelector('i');
        if (theme === 'dark-mode') {
            icon.className = 'fa-solid fa-sun text-warning';
        } else {
            icon.className = 'fa-solid fa-moon text-accent';
        }
    }

    // === 2. GLOBAL UTILITY: TOAST NOTIFICATIONS ===
    window.showToast = function (message, type = 'info') {
        const toastEl = document.getElementById('app-toast');
        if (!toastEl) return;
        
        const toastMessageEl = document.getElementById('toast-message');
        const toastIconEl = document.getElementById('toast-icon');
        
        toastMessageEl.textContent = message;
        
        // Set type classes
        if (type === 'success') {
            toastIconEl.className = 'fa-solid fa-circle-check text-success-custom me-2';
        } else if (type === 'error') {
            toastIconEl.className = 'fa-solid fa-circle-exclamation text-danger me-2';
        } else {
            toastIconEl.className = 'fa-solid fa-info-circle text-primary me-2';
        }
        
        const bsToast = new bootstrap.Toast(toastEl, { delay: 3000 });
        bsToast.show();
    };

    // === 3. GLOBAL UTILITY: LOADING OVERLAY ===
    window.toggleLoading = function (show) {
        const overlay = document.getElementById('loading-overlay');
        if (!overlay) return;
        if (show) {
            overlay.classList.remove('d-none');
        } else {
            overlay.classList.add('d-none');
        }
    };

    // === 4. BMI PAGE FORM SUBMISSION ===
    const bmiForm = document.getElementById('bmi-form');
    const bmiResultPanel = document.getElementById('bmi-result-panel');
    
    if (bmiForm) {
        bmiForm.addEventListener('submit', function (e) {
            e.preventDefault();
            
            if (!bmiForm.checkValidity()) {
                e.stopPropagation();
                bmiForm.classList.add('was-validated');
                return;
            }
            
            const weight = parseFloat(document.getElementById('weight').value);
            const height = parseFloat(document.getElementById('height').value);
            const age = parseInt(document.getElementById('age').value);
            const gender = document.querySelector('input[name="gender"]:checked').value;
            const activity = document.getElementById('activity').value;
            
            toggleLoading(true);
            
            fetch('/api/bmi', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ weight, height, age, gender, activity })
            })
            .then(res => res.json())
            .then(data => {
                toggleLoading(false);
                if (data.success) {
                    // Populate BMI results
                    document.getElementById('result-bmi-val').textContent = data.bmi;
                    document.getElementById('result-tdee-val').textContent = Math.round(data.tdee).toLocaleString('vi-VN');
                    document.getElementById('result-bmr-val').textContent = Math.round(data.bmr).toLocaleString('vi-VN');
                    
                    // Lượng nước
                    const water = (weight * 0.04).toFixed(1);
                    document.getElementById('result-water-val').textContent = water;
                    
                    // Set classification badge style
                    const badge = document.getElementById('result-bmi-badge');
                    badge.textContent = data.classification;
                    badge.className = 'badge px-4 py-2 fs-6 rounded-pill';
                    
                    if (data.classification === 'Gầy') {
                        badge.classList.add('bg-info', 'text-white');
                    } else if (data.classification === 'Bình thường') {
                        badge.classList.add('bg-success', 'text-white');
                    } else if (data.classification === 'Thừa cân') {
                        badge.classList.add('bg-warning', 'text-dark');
                    } else {
                        badge.classList.add('bg-danger', 'text-white');
                    }
                    
                    // Reveal result panel
                    bmiResultPanel.classList.remove('d-none');
                    bmiResultPanel.scrollIntoView({ behavior: 'smooth' });
                    showToast("Tính chỉ số BMI thành công!", "success");
                    
                    // Save query parameters to forward to recommend
                    const btnGoRecommend = document.getElementById('btn-go-recommend');
                    if (btnGoRecommend) {
                        btnGoRecommend.onclick = function() {
                            window.location.href = `/recommend?height=${height}&weight=${weight}&age=${age}&gender=${gender}&activity=${activity}`;
                        };
                    }
                } else {
                    showToast(data.error || "Lỗi khi tính BMI.", "error");
                }
            })
            .catch(err => {
                toggleLoading(false);
                showToast("Lỗi kết nối máy chủ.", "error");
                console.error(err);
            });
        });
    }

    // === 5. RECOMMEND PAGE CODE ===
    const recommendForm = document.getElementById('recommend-form');
    const placeholderPanel = document.getElementById('recommend-placeholder');
    const resultPanel = document.getElementById('recommend-result-container');
    
    // Parse URL params on load to autofill recommend form
    if (recommendForm) {
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('height')) {
            document.getElementById('height').value = urlParams.get('height');
            document.getElementById('weight').value = urlParams.get('weight');
            document.getElementById('age').value = urlParams.get('age');
            document.getElementById('gender').value = urlParams.get('gender');
            document.getElementById('activity').value = urlParams.get('activity');
            
            // Auto submit
            setTimeout(() => {
                recommendForm.dispatchEvent(new Event('submit'));
            }, 300);
        }
        
        recommendForm.addEventListener('submit', function (e) {
            e.preventDefault();
            if (!recommendForm.checkValidity()) {
                e.stopPropagation();
                recommendForm.classList.add('was-validated');
                return;
            }
            
            generateMenu();
        });
    }
    
    let currentRecMenu = null; // Store menu details globally on page
    let macroChartInstance = null;
    let calorieChartInstance = null;

    function generateMenu() {
        const weight = parseFloat(document.getElementById('weight').value);
        const height = parseFloat(document.getElementById('height').value);
        const age = parseInt(document.getElementById('age').value);
        const gender = document.getElementById('gender').value;
        const activity = document.getElementById('activity').value;
        const budget = parseFloat(document.getElementById('budget').value);
        const goal = document.getElementById('goal').value;
        
        toggleLoading(true);
        
        fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ weight, height, age, gender, activity, budget, goal })
        })
        .then(res => res.json())
        .then(data => {
            toggleLoading(false);
            if (data.success) {
                currentRecMenu = data;
                renderMealPlanDashboard(data);
                if (data.warning) {
                    showToast(data.warning, "warning");
                } else {
                    showToast("Tạo thực đơn thành công!", "success");
                }
            } else {
                showToast(data.error || "Không tìm thấy thực đơn phù hợp.", "error");
            }
        })
        .catch(err => {
            toggleLoading(false);
            showToast("Lỗi kết nối máy chủ.", "error");
            console.error(err);
        });
    }

    function renderMealPlanDashboard(data) {
        placeholderPanel.classList.add('d-none');
        resultPanel.classList.remove('d-none');
        
        // Fill header metrics
        document.getElementById('metric-bmi-class').textContent = data.classification || 'Bình thường';
        document.getElementById('metric-tdee').textContent = Math.round(data.tdee || 0).toLocaleString('vi-VN');
        document.getElementById('metric-target-calories').textContent = Math.round(data.target_calories || 0).toLocaleString('vi-VN');
        
        // Render food cards
        const cardsGrid = document.getElementById('menu-cards-grid');
        cardsGrid.innerHTML = '';
        
        const meals = [
            { key: 'breakfast', name: 'Bữa Sáng', icon: 'fa-egg', color: 'bg-success-light text-success-custom' },
            { key: 'lunch', name: 'Bữa Trưa', icon: 'fa-utensils', color: 'bg-accent-light text-accent' },
            { key: 'dinner', name: 'Bữa Tối', icon: 'fa-bowl-rice', color: 'bg-success-light text-success-custom' },
            { key: 'snack', name: 'Bữa Phụ / Nước', icon: 'fa-mug-hot', color: 'bg-accent-light text-accent' }
        ];
        
        meals.forEach(m => {
            const food = data[m.key];
            if (!food) {
                return;
            }
            const col = document.createElement('div');
            col.className = 'col-md-6 col-xl-3 fade-in';
            col.innerHTML = `
                <div class="card h-100 hover-card border-0 glass-card p-4 shadow-sm position-relative">
                    <span class="badge ${m.color} meal-badge"><i class="fa-solid ${m.icon} me-1"></i>${m.name}</span>
                    <div class="mt-3">
                        <h5 class="fw-extrabold text-body-custom mt-3 mb-1" style="height: 48px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                            ${food.name}
                        </h5>
                        <p class="text-accent fw-bold fs-5 mb-3">${Math.round(food.price).toLocaleString('vi-VN')} đ</p>
                        
                        <div class="border-top pt-2">
                            <div class="d-flex justify-content-between py-1 small">
                                <span class="text-muted">Năng lượng:</span>
                                <span class="fw-semibold text-body-custom">${food.calories} kcal</span>
                            </div>
                            <div class="d-flex justify-content-between py-1 small">
                                <span class="text-muted">Chất đạm (Protein):</span>
                                <span class="fw-semibold text-body-custom">${food.protein}g</span>
                            </div>
                            <div class="d-flex justify-content-between py-1 small">
                                <span class="text-muted">Chất béo (Fat):</span>
                                <span class="fw-semibold text-body-custom">${food.fat}g</span>
                            </div>
                            <div class="d-flex justify-content-between py-1 small">
                                <span class="text-muted">Tinh bột (Carb):</span>
                                <span class="fw-semibold text-body-custom">${food.carb}g</span>
                            </div>
                            <div class="d-flex justify-content-between py-1 small">
                                <span class="text-muted">Chất xơ:</span>
                                <span class="fw-semibold text-body-custom">${food.fiber}g</span>
                            </div>
                            <div class="d-flex justify-content-between py-1 small">
                                <span class="text-muted">Vitamin:</span>
                                <span class="fw-semibold text-body-custom text-truncate" style="max-width: 120px;" title="${food.vitamin}">${food.vitamin}</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            cardsGrid.appendChild(col);
        });
        
        // Render Charts
        renderCharts(data);
    }

    function renderCharts(data) {
        const metrics = data.metrics;
        
        // --- 1. MACRO PIE CHART ---
        const ctxPie = document.getElementById('macroPieChart').getContext('2d');
        if (macroChartInstance) {
            macroChartInstance.destroy();
        }
        
        // Calories from each macro: Protein = 4 kcal/g, Carb = 4 kcal/g, Fat = 9 kcal/g
        const protKcal = metrics.total_protein * 4;
        const carbKcal = metrics.total_carb * 4;
        const fatKcal = metrics.total_fat * 9;
        const totalMacroKcal = protKcal + carbKcal + fatKcal;
        
        const protPct = Math.round((protKcal / totalMacroKcal) * 100);
        const carbPct = Math.round((carbKcal / totalMacroKcal) * 100);
        const fatPct = 100 - protPct - carbPct;
        
        const isDark = document.body.classList.contains('dark-mode');
        const textColor = isDark ? '#f1f5f9' : '#2c3e50';
        
        macroChartInstance = new Chart(ctxPie, {
            type: 'doughnut',
            data: {
                labels: [`Protein (${metrics.total_protein}g - ${protPct}%)`, `Carb (${metrics.total_carb}g - ${carbPct}%)`, `Fat (${metrics.total_fat}g - ${fatPct}%)`],
                datasets: [{
                    data: [protKcal, carbKcal, fatKcal],
                    backgroundColor: ['#27ae60', '#e67e22', '#f1c40f'],
                    borderWidth: 1,
                    borderColor: isDark ? '#1e293b' : '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: textColor, font: { family: 'Outfit', size: 12 } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Năng lượng: ${Math.round(context.raw)} kcal`;
                            }
                        }
                    }
                }
            }
        });
        
        // --- 2. CALORIE & COST COMPARISON BAR CHART ---
        const ctxBar = document.getElementById('calorieBarChart').getContext('2d');
        if (calorieChartInstance) {
            calorieChartInstance.destroy();
        }
        
        const budgetTarget = parseFloat(document.getElementById('budget').value);
        
        calorieChartInstance = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['Năng lượng (kcal)', 'Chi phí (đ x10)'],
                datasets: [
                    {
                        label: 'Mục tiêu',
                        data: [data.target_calories, budgetTarget / 10],
                        backgroundColor: '#bdc3c7',
                        borderRadius: 8
                    },
                    {
                        label: 'Thực tế thực đơn',
                        data: [metrics.total_calories, metrics.total_cost / 10],
                        backgroundColor: '#27ae60',
                        borderRadius: 8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: textColor }
                    },
                    x: {
                        ticks: { color: textColor }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: textColor, font: { family: 'Outfit' } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let val = context.raw;
                                if (context.dataIndex === 1) {
                                    return `${context.dataset.label}: ${(val * 10).toLocaleString('vi-VN')} đ`;
                                }
                                return `${context.dataset.label}: ${Math.round(val)} kcal`;
                            }
                        }
                    }
                }
            }
        });
    }

    // === 6. ACTION HANDLERS (REGENERATE, PRINT, DOWNLOAD) ===
    const btnRegenerate = document.getElementById('btn-regenerate');
    if (btnRegenerate) {
        btnRegenerate.addEventListener('click', function() {
            generateMenu();
        });
    }
    
    const btnPrint = document.getElementById('btn-print-menu');
    if (btnPrint) {
        btnPrint.addEventListener('click', function() {
            window.print();
        });
    }
    
    const btnDownload = document.getElementById('btn-download-csv');
    if (btnDownload) {
        btnDownload.addEventListener('click', function() {
            if (!currentRecMenu) return;
            
            // Format CSV content
            let csvContent = "data:text/csv;charset=utf-8,\uFEFF"; // Add BOM for Excel UTF-8 representation
            csvContent += "Bữa ăn,Tên món ăn,Giá (VND),Năng lượng (kcal),Protein (g),Carb (g),Fat (g),Chất xơ (g),Vitamin\r\n";
            
            const meals = ['breakfast', 'lunch', 'dinner', 'snack'];
            const mealNames = ['Bữa Sáng', 'Bữa Trưa', 'Bữa Tối', 'Bữa Phụ - Nước'];
            
            meals.forEach((m, idx) => {
                const item = currentRecMenu[m];
                csvContent += `"${mealNames[idx]}","${item.name}",${item.price},${item.calories},${item.protein},${item.carb},${item.fat},${item.fiber},"${item.vitamin}"\r\n`;
            });
            
            csvContent += `\r\n"TỔNG CỘNG",,${currentRecMenu.metrics.total_cost},${currentRecMenu.metrics.total_calories},${currentRecMenu.metrics.total_protein},${currentRecMenu.metrics.total_carb},${currentRecMenu.metrics.total_fat},${currentRecMenu.metrics.total_fiber}\r\n`;
            
            // Trigger download
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "thuc_don_uth.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            showToast("Tải file CSV thành công!", "success");
        });
    }

    // === 7. SEEDED FOOD DATABASE SEARCH DIRECTORY ===
    const btnSearchFoods = document.getElementById('btn-search-foods');
    const resultsGrid = document.getElementById('search-results-grid');
    
    if (resultsGrid) {
        // Run initial empty search to populate card list on load
        searchFoods();
        
        if (btnSearchFoods) {
            btnSearchFoods.addEventListener('click', searchFoods);
        }
        
        // Debounce search on text entry
        let searchTimeout;
        const textInput = document.getElementById('search-food-name');
        if (textInput) {
            textInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(searchFoods, 400);
            });
        }
    }
    
    function searchFoods() {
        const q = document.getElementById('search-food-name').value;
        const category = document.getElementById('search-food-category').value;
        const maxPrice = document.getElementById('search-food-max-price').value;
        const maxCal = document.getElementById('search-food-max-cal').value;
        
        let url = `/api/foods?q=${encodeURIComponent(q)}&category=${category}`;
        if (maxPrice) url += `&max_price=${maxPrice}`;
        if (maxCal) url += `&max_calories=${maxCal}`;
        
        fetch(url)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                resultsGrid.innerHTML = '';
                if (data.foods.length === 0) {
                    resultsGrid.innerHTML = `
                        <div class="col-12 text-center text-muted py-4">
                            <i class="fa-solid fa-face-frown fs-2 mb-2"></i>
                            <p>Không tìm thấy món ăn nào khớp với bộ lọc.</p>
                        </div>
                    `;
                    return;
                }
                
                data.foods.forEach(f => {
                    const col = document.createElement('div');
                    col.className = 'col-sm-6 col-lg-4 col-xl-3';
                    
                    let catColor = 'bg-success-light text-success-custom';
                    if (f.category === 'Trưa/Tối') catColor = 'bg-accent-light text-accent';
                    
                    col.innerHTML = `
                        <div class="card h-100 hover-card border-0 glass-card p-3 shadow-sm position-relative">
                            <span class="badge ${catColor} position-absolute" style="top:10px; right:10px; font-size:0.7rem;">${f.category}</span>
                            <div class="pt-2">
                                <h6 class="fw-bold text-body-custom mb-1 text-truncate" title="${f.name}">${f.name}</h6>
                                <p class="text-accent fw-bold small mb-2">${Math.round(f.price).toLocaleString('vi-VN')} đ</p>
                                <div class="border-top pt-2 small text-muted">
                                    <div class="d-flex justify-content-between">
                                        <span>Calo:</span> <span class="fw-semibold text-body-custom">${f.calories} kcal</span>
                                    </div>
                                    <div class="d-flex justify-content-between">
                                        <span>Protein:</span> <span class="fw-semibold text-body-custom">${f.protein}g</span>
                                    </div>
                                    <div class="d-flex justify-content-between">
                                        <span>Carb/Fat:</span> <span class="fw-semibold text-body-custom">${f.carb}g / ${f.fat}g</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    resultsGrid.appendChild(col);
                });
            }
        })
        .catch(err => {
            console.error("Error searching foods:", err);
        });
    }
});
