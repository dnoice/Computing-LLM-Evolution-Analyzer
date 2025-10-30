/**
 * Computing Evolution Dashboard - Chart.js Configurations
 *
 * This file handles all Chart.js visualizations including:
 * - Hardware evolution charts
 * - GPU performance charts
 * - LLM scaling charts
 * - Cloud cost analysis charts
 * - Comparison charts
 */

// Global chart instances
const chartInstances = {};

// Chart color schemes
const chartColors = {
    primary: '#3b82f6',
    secondary: '#8b5cf6',
    accent: '#06b6d4',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    blue: '#3b82f6',
    purple: '#8b5cf6',
    cyan: '#06b6d4',
    green: '#10b981',
    yellow: '#f59e0b',
    red: '#ef4444',
    pink: '#ec4899',
    indigo: '#6366f1',
    teal: '#14b8a6',
    orange: '#f97316'
};

// Default chart options
const defaultChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    interaction: {
        mode: 'index',
        intersect: false,
    },
    plugins: {
        legend: {
            display: true,
            position: 'top',
            labels: {
                usePointStyle: true,
                padding: 15,
                font: {
                    size: 12,
                    weight: '500'
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            titleFont: {
                size: 14,
                weight: 'bold'
            },
            bodyFont: {
                size: 13
            },
            borderColor: chartColors.primary,
            borderWidth: 1,
            displayColors: true,
            callbacks: {}
        }
    },
    scales: {
        x: {
            grid: {
                display: false
            },
            ticks: {
                font: {
                    size: 11
                }
            }
        },
        y: {
            beginAtZero: true,
            grid: {
                color: 'rgba(0, 0, 0, 0.05)'
            },
            ticks: {
                font: {
                    size: 11
                }
            }
        }
    }
};

/**
 * Safely get canvas context with error handling
 */
function getCanvasContext(id) {
    const canvas = document.getElementById(id);
    if (!canvas) {
        console.warn(`Canvas element not found: ${id}`);
        return null;
    }
    return canvas;
}

/**
 * Safely destroy chart instance
 */
function destroyChart(chartName) {
    if (chartInstances[chartName]) {
        try {
            chartInstances[chartName].destroy();
            delete chartInstances[chartName];
        } catch (error) {
            console.error(`Error destroying chart ${chartName}:`, error);
        }
    }
}

/**
 * Initialize all charts with error handling
 */
function initializeCharts() {
    try {
        initializeMooresLawChart();
        initializeHardwareCharts();
        initializeGPUCharts();
        initializeLLMCharts();
        initializeCloudCharts();
        initializeComparisonChart();
        console.log('All charts initialized successfully');
    } catch (error) {
        console.error('Error initializing charts:', error);
    }
}

/**
 * Moore's Law Chart
 */
function initializeMooresLawChart() {
    const ctx = getCanvasContext('mooresLawChart');
    if (!ctx) return;

    try {
        destroyChart('mooresLaw');

    const data = window.hardwareData || getSampleHardwareData();
    const years = data.map(d => d.year);
    const transistors = data.map(d => d.cpu_transistors || d.transistors || 0);

    // Moore's Law prediction (doubles every 2 years)
    const startYear = Math.min(...years);
    const endYear = Math.max(...years) + 10;
    const startTransistors = transistors[0];
    const predictionYears = [];
    const predictionValues = [];

    for (let year = startYear; year <= endYear; year += 2) {
        predictionYears.push(year);
        const yearsSinceStart = year - startYear;
        const doublings = yearsSinceStart / 2;
        predictionValues.push(startTransistors * Math.pow(2, doublings));
    }

    chartInstances.mooresLaw = new Chart(ctx, {
        type: 'line',
        data: {
            labels: years.concat(predictionYears.slice(years.length)),
            datasets: [
                {
                    label: 'Actual Transistor Count',
                    data: transistors,
                    borderColor: chartColors.primary,
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    borderWidth: 3,
                    tension: 0.4
                },
                {
                    label: 'Moore\'s Law Prediction',
                    data: Array(years.length - 1).fill(null).concat(predictionValues.slice(years.length - 1)),
                    borderColor: chartColors.warning,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    borderWidth: 2,
                    tension: 0.4
                }
            ]
        },
        options: {
            ...defaultChartOptions,
            scales: {
                ...defaultChartOptions.scales,
                y: {
                    ...defaultChartOptions.scales.y,
                    type: 'logarithmic',
                    title: {
                        display: true,
                        text: 'Transistor Count (log scale)',
                        font: {
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return formatNumber(value);
                        }
                    }
                }
            },
            plugins: {
                ...defaultChartOptions.plugins,
                tooltip: {
                    ...defaultChartOptions.plugins.tooltip,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + formatNumber(context.parsed.y) + ' transistors';
                        }
                    }
                }
            }
        }
    });
    } catch (error) {
        console.error('Error initializing Moore\'s Law chart:', error);
    }
}

/**
 * Hardware Evolution Charts
 */
function initializeHardwareCharts() {
    const data = window.hardwareData || getSampleHardwareData();
    const years = data.map(d => d.year);

    // Transistor Chart
    const transistorCtx = document.getElementById('transistorChart');
    if (transistorCtx) {
        const transistors = data.map(d => d.cpu_transistors || d.transistors || 0);
        chartInstances.transistor = new Chart(transistorCtx, {
            type: 'line',
            data: {
                labels: years,
                datasets: [{
                    label: 'Transistor Count',
                    data: transistors,
                    borderColor: chartColors.blue,
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3,
                    pointRadius: 4
                }]
            },
            options: {
                ...defaultChartOptions,
                scales: {
                    ...defaultChartOptions.scales,
                    y: {
                        ...defaultChartOptions.scales.y,
                        type: 'logarithmic',
                        title: {
                            display: true,
                            text: 'Transistors (log scale)'
                        }
                    }
                }
            }
        });
    }

    // Clock Speed Chart
    const clockCtx = document.getElementById('clockSpeedChart');
    if (clockCtx) {
        const clockSpeeds = data.map(d => d.cpu_clock_mhz || d.clock_speed || 0);
        chartInstances.clockSpeed = new Chart(clockCtx, {
            type: 'bar',
            data: {
                labels: years,
                datasets: [{
                    label: 'Clock Speed (MHz)',
                    data: clockSpeeds,
                    backgroundColor: chartColors.purple,
                    borderColor: chartColors.purple,
                    borderWidth: 2,
                    borderRadius: 6
                }]
            },
            options: defaultChartOptions
        });
    }

    // RAM Chart
    const ramCtx = document.getElementById('ramChart');
    if (ramCtx) {
        const ramSizes = data.map(d => d.ram_mb || d.ram || 0);
        chartInstances.ram = new Chart(ramCtx, {
            type: 'line',
            data: {
                labels: years,
                datasets: [{
                    label: 'RAM (MB)',
                    data: ramSizes,
                    borderColor: chartColors.cyan,
                    backgroundColor: 'rgba(6, 182, 212, 0.2)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3
                }]
            },
            options: {
                ...defaultChartOptions,
                scales: {
                    ...defaultChartOptions.scales,
                    y: {
                        ...defaultChartOptions.scales.y,
                        type: 'logarithmic',
                        title: {
                            display: true,
                            text: 'RAM MB (log scale)'
                        }
                    }
                }
            }
        });
    }

    // Price/Performance Chart
    const priceCtx = document.getElementById('pricePerformanceChart');
    if (priceCtx) {
        const prices = data.map(d => d.price_usd || 0);
        chartInstances.pricePerformance = new Chart(priceCtx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Price vs Performance',
                    data: data.map((d, i) => ({
                        x: d.cpu_clock_mhz || d.clock_speed || 0,
                        y: d.price_usd || 0
                    })),
                    backgroundColor: chartColors.green,
                    borderColor: chartColors.green,
                    pointRadius: 8,
                    pointHoverRadius: 12
                }]
            },
            options: {
                ...defaultChartOptions,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Clock Speed (MHz)'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Price (USD)'
                        }
                    }
                }
            }
        });
    }
}

/**
 * GPU Charts
 */
function initializeGPUCharts() {
    const data = window.gpuData || getSampleGPUData();
    updateGPUChartsWithFilter('all');
}

function updateGPUChartsWithFilter(filter) {
    let data = window.gpuData || getSampleGPUData();

    // Filter data by manufacturer
    if (filter !== 'all') {
        data = data.filter(d => d.manufacturer?.toLowerCase() === filter.toLowerCase());
    }

    const years = data.map(d => d.year);
    const manufacturers = [...new Set(data.map(d => d.manufacturer))];

    // TFLOPS Chart
    const tflopsCtx = document.getElementById('gpuTflopsChart');
    if (tflopsCtx) {
        if (chartInstances.gpuTflops) chartInstances.gpuTflops.destroy();

        const datasets = manufacturers.map((mfr, i) => {
            const mfrData = data.filter(d => d.manufacturer === mfr);
            return {
                label: mfr,
                data: mfrData.map(d => ({x: d.year, y: d.tflops_fp32 || 0})),
                borderColor: Object.values(chartColors)[i % 10],
                backgroundColor: `${Object.values(chartColors)[i % 10]}33`,
                tension: 0.4,
                borderWidth: 3
            };
        });

        chartInstances.gpuTflops = new Chart(tflopsCtx, {
            type: 'line',
            data: { datasets },
            options: {
                ...defaultChartOptions,
                scales: {
                    ...defaultChartOptions.scales,
                    y: {
                        title: {
                            display: true,
                            text: 'TFLOPS (FP32)'
                        }
                    }
                }
            }
        });
    }

    // VRAM Chart
    const vramCtx = document.getElementById('gpuVramChart');
    if (vramCtx) {
        if (chartInstances.gpuVram) chartInstances.gpuVram.destroy();

        chartInstances.gpuVram = new Chart(vramCtx, {
            type: 'bar',
            data: {
                labels: data.map(d => `${d.name} (${d.year})`),
                datasets: [{
                    label: 'VRAM (GB)',
                    data: data.map(d => d.vram_gb || 0),
                    backgroundColor: chartColors.purple,
                    borderRadius: 6
                }]
            },
            options: {
                ...defaultChartOptions,
                indexAxis: data.length > 15 ? 'y' : 'x'
            }
        });
    }

    // Efficiency Chart
    const efficiencyCtx = document.getElementById('gpuEfficiencyChart');
    if (efficiencyCtx) {
        if (chartInstances.gpuEfficiency) chartInstances.gpuEfficiency.destroy();

        chartInstances.gpuEfficiency = new Chart(efficiencyCtx, {
            type: 'scatter',
            data: {
                datasets: manufacturers.map((mfr, i) => {
                    const mfrData = data.filter(d => d.manufacturer === mfr && d.tdp_watts);
                    return {
                        label: mfr,
                        data: mfrData.map(d => ({
                            x: d.year,
                            y: (d.tflops_fp32 || 0) / (d.tdp_watts || 1)
                        })),
                        backgroundColor: Object.values(chartColors)[i % 10],
                        borderColor: Object.values(chartColors)[i % 10],
                        pointRadius: 8
                    };
                })
            },
            options: {
                ...defaultChartOptions,
                scales: {
                    ...defaultChartOptions.scales,
                    y: {
                        title: {
                            display: true,
                            text: 'TFLOPS per Watt'
                        }
                    }
                }
            }
        });
    }

    // Manufacturer Comparison
    const mfrCtx = document.getElementById('gpuManufacturerChart');
    if (mfrCtx) {
        if (chartInstances.gpuManufacturer) chartInstances.gpuManufacturer.destroy();

        const avgTflops = manufacturers.map(mfr => {
            const mfrData = data.filter(d => d.manufacturer === mfr);
            const sum = mfrData.reduce((acc, d) => acc + (d.tflops_fp32 || 0), 0);
            return sum / mfrData.length;
        });

        chartInstances.gpuManufacturer = new Chart(mfrCtx, {
            type: 'doughnut',
            data: {
                labels: manufacturers,
                datasets: [{
                    label: 'Average TFLOPS',
                    data: avgTflops,
                    backgroundColor: manufacturers.map((_, i) => Object.values(chartColors)[i % 10]),
                    borderWidth: 3,
                    borderColor: '#fff'
                }]
            },
            options: {
                ...defaultChartOptions,
                plugins: {
                    ...defaultChartOptions.plugins,
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

/**
 * LLM Charts
 */
function initializeLLMCharts() {
    const data = window.llmData || getSampleLLMData();
    const models = data.map(d => d.name);

    // Parameters Chart
    const paramsCtx = document.getElementById('llmParametersChart');
    if (paramsCtx) {
        chartInstances.llmParameters = new Chart(paramsCtx, {
            type: 'bar',
            data: {
                labels: models,
                datasets: [{
                    label: 'Parameters (Billions)',
                    data: data.map(d => d.parameters_billions || 0),
                    backgroundColor: chartColors.blue,
                    borderRadius: 8
                }]
            },
            options: {
                ...defaultChartOptions,
                indexAxis: 'y',
                scales: {
                    x: {
                        type: 'logarithmic',
                        title: {
                            display: true,
                            text: 'Parameters (Billions, log scale)'
                        }
                    }
                }
            }
        });
    }

    // Training Compute Chart
    const computeCtx = document.getElementById('llmComputeChart');
    if (computeCtx) {
        chartInstances.llmCompute = new Chart(computeCtx, {
            type: 'line',
            data: {
                labels: data.map(d => d.year),
                datasets: [{
                    label: 'Training Compute (FLOPs)',
                    data: data.map(d => d.training_compute_flops || 0),
                    borderColor: chartColors.purple,
                    backgroundColor: 'rgba(139, 92, 246, 0.2)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3
                }]
            },
            options: {
                ...defaultChartOptions,
                scales: {
                    ...defaultChartOptions.scales,
                    y: {
                        type: 'logarithmic',
                        title: {
                            display: true,
                            text: 'FLOPs (log scale)'
                        }
                    }
                }
            }
        });
    }

    // Context Window Chart
    const contextCtx = document.getElementById('llmContextChart');
    if (contextCtx) {
        chartInstances.llmContext = new Chart(contextCtx, {
            type: 'bar',
            data: {
                labels: models,
                datasets: [{
                    label: 'Context Window (tokens)',
                    data: data.map(d => d.context_window || 0),
                    backgroundColor: chartColors.cyan,
                    borderRadius: 6
                }]
            },
            options: {
                ...defaultChartOptions,
                scales: {
                    y: {
                        type: 'logarithmic'
                    }
                }
            }
        });
    }

    // Capability Radar Chart
    const capabilityCtx = document.getElementById('llmCapabilityChart');
    if (capabilityCtx) {
        const latestModels = data.slice(-5);

        // Helper function to estimate capability scores based on model parameters and year
        const estimateCapabilityScore = (model, capability) => {
            // If actual score exists, use it
            const actualScore = model[`${capability}_score`] || model.capability_score;
            if (actualScore) return actualScore;

            // Otherwise estimate based on parameters and year
            const params = model.parameters_billions || 1;
            const year = model.year || 2020;
            const yearFactor = Math.min((year - 2018) / 6, 1); // Normalize year (2018-2024)
            const paramFactor = Math.min(Math.log10(params + 1) / 3, 1); // Normalize params (log scale)

            // Base score increases with both parameters and recency
            const baseScore = 50 + (yearFactor * 25) + (paramFactor * 25);

            // Adjust by capability type (some models are better at certain tasks)
            const adjustments = {
                'reasoning': model.organization === 'OpenAI' ? 5 : 0,
                'coding': model.organization === 'OpenAI' ? 5 : model.organization === 'Anthropic' ? 3 : 0,
                'math': params > 100 ? 5 : 0,
                'language': model.organization === 'Anthropic' ? 5 : 0,
                'knowledge': params > 50 ? 5 : 0
            };

            return Math.min(baseScore + (adjustments[capability] || 0), 100);
        };

        chartInstances.llmCapability = new Chart(capabilityCtx, {
            type: 'radar',
            data: {
                labels: ['Reasoning', 'Coding', 'Math', 'Language', 'Knowledge'],
                datasets: latestModels.map((model, i) => ({
                    label: model.name,
                    data: [
                        estimateCapabilityScore(model, 'reasoning'),
                        estimateCapabilityScore(model, 'coding'),
                        estimateCapabilityScore(model, 'math'),
                        estimateCapabilityScore(model, 'language'),
                        estimateCapabilityScore(model, 'knowledge')
                    ],
                    borderColor: Object.values(chartColors)[i % 10],
                    backgroundColor: `${Object.values(chartColors)[i % 10]}33`,
                    borderWidth: 2
                }))
            },
            options: {
                ...defaultChartOptions,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20
                        }
                    }
                },
                plugins: {
                    ...defaultChartOptions.plugins,
                    tooltip: {
                        ...defaultChartOptions.plugins.tooltip,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.r.toFixed(0) + '/100';
                            }
                        }
                    }
                }
            }
        });
    }
}

/**
 * Cloud Cost Charts
 */
function initializeCloudCharts() {
    const data = window.cloudData || getSampleCloudData();
    const providers = [...new Set(data.map(d => d.provider))];

    // Provider Comparison
    const providerCtx = document.getElementById('cloudProviderChart');
    if (providerCtx) {
        const avgCost = providers.map(provider => {
            const providerData = data.filter(d => d.provider === provider);
            const sum = providerData.reduce((acc, d) => acc + (d.on_demand_hourly || 0), 0);
            return sum / providerData.length;
        });

        chartInstances.cloudProvider = new Chart(providerCtx, {
            type: 'bar',
            data: {
                labels: providers,
                datasets: [{
                    label: 'Average On-Demand Cost ($/hour)',
                    data: avgCost,
                    backgroundColor: [chartColors.orange, chartColors.blue, chartColors.red],
                    borderRadius: 8,
                    borderWidth: 2
                }]
            },
            options: defaultChartOptions
        });
    }

    // Spot Savings
    const spotCtx = document.getElementById('spotSavingsChart');
    if (spotCtx) {
        const savings = data.map(d => {
            const onDemand = d.on_demand_hourly || 0;
            const spot = d.spot_hourly || 0;
            return onDemand > 0 ? ((onDemand - spot) / onDemand) * 100 : 0;
        });

        chartInstances.spotSavings = new Chart(spotCtx, {
            type: 'bar',
            data: {
                labels: data.map(d => `${d.provider} ${d.instance_type}`),
                datasets: [{
                    label: 'Spot Savings (%)',
                    data: savings,
                    backgroundColor: chartColors.green,
                    borderRadius: 6
                }]
            },
            options: {
                ...defaultChartOptions,
                indexAxis: 'y'
            }
        });
    }

    // Instance Comparison
    const instanceCtx = document.getElementById('instanceComparisonChart');
    if (instanceCtx) {
        chartInstances.instanceComparison = new Chart(instanceCtx, {
            type: 'scatter',
            data: {
                datasets: providers.map((provider, i) => {
                    const providerData = data.filter(d => d.provider === provider);
                    return {
                        label: provider,
                        data: providerData.map(d => ({
                            x: d.tflops || 0,
                            y: d.on_demand_hourly || 0
                        })),
                        backgroundColor: [chartColors.orange, chartColors.blue, chartColors.red][i],
                        borderColor: [chartColors.orange, chartColors.blue, chartColors.red][i],
                        pointRadius: 10,
                        pointHoverRadius: 14
                    };
                })
            },
            options: {
                ...defaultChartOptions,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'TFLOPS'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Cost ($/hour)'
                        }
                    }
                }
            }
        });
    }

    // Pricing Trends
    const trendsCtx = document.getElementById('pricingTrendsChart');
    if (trendsCtx) {
        chartInstances.pricingTrends = new Chart(trendsCtx, {
            type: 'line',
            data: {
                labels: data.map(d => d.year || '2024'),
                datasets: providers.map((provider, i) => {
                    const providerData = data.filter(d => d.provider === provider);
                    return {
                        label: provider,
                        data: providerData.map(d => d.on_demand_hourly || 0),
                        borderColor: [chartColors.orange, chartColors.blue, chartColors.red][i],
                        tension: 0.4,
                        borderWidth: 3
                    };
                })
            },
            options: defaultChartOptions
        });
    }
}

/**
 * Comparison Chart
 */
function initializeComparisonChart() {
    const ctx = document.getElementById('comparisonChart');
    if (!ctx) return;

    // Initial empty chart
    chartInstances.comparison = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: []
        },
        options: defaultChartOptions
    });
}

function updateComparisonChartData(type, metric) {
    if (!chartInstances.comparison) return;

    let data, labels, values, chartLabel;

    switch (type) {
        case 'hardware':
            data = window.hardwareData || getSampleHardwareData();
            labels = data.map(d => `${d.name} (${d.year})`);
            if (metric === 'performance') {
                values = data.map(d => d.cpu_clock_mhz || 0);
                chartLabel = 'Clock Speed (MHz)';
            } else if (metric === 'efficiency') {
                values = data.map(d => (d.cpu_transistors || 0) / (d.price_usd || 1));
                chartLabel = 'Transistors per Dollar';
            } else if (metric === 'cost') {
                values = data.map(d => d.price_usd || 0);
                chartLabel = 'Price (USD)';
            } else {
                values = data.map(d => d.cpu_transistors || 0);
                chartLabel = 'Transistor Count';
            }
            break;

        case 'gpu':
            data = window.gpuData || getSampleGPUData();
            labels = data.map(d => `${d.name} (${d.year})`);
            if (metric === 'performance') {
                values = data.map(d => d.tflops_fp32 || 0);
                chartLabel = 'TFLOPS (FP32)';
            } else if (metric === 'efficiency') {
                values = data.map(d => (d.tflops_fp32 || 0) / (d.tdp_watts || 1));
                chartLabel = 'TFLOPS per Watt';
            } else if (metric === 'cost') {
                values = data.map(d => d.price_usd || 0);
                chartLabel = 'Price (USD)';
            } else {
                values = data.map(d => d.vram_gb || 0);
                chartLabel = 'VRAM (GB)';
            }
            break;

        case 'llm':
            data = window.llmData || getSampleLLMData();
            labels = data.map(d => `${d.name} (${d.year})`);
            if (metric === 'performance') {
                values = data.map(d => d.parameters_billions || 0);
                chartLabel = 'Parameters (Billions)';
            } else if (metric === 'efficiency') {
                values = data.map(d => {
                    const params = d.parameters_billions || 1;
                    const compute = d.training_compute_flops || 1;
                    return params / Math.log10(compute);
                });
                chartLabel = 'Parameter Efficiency';
            } else if (metric === 'cost') {
                values = data.map(d => {
                    // Estimate cost based on training compute (rough estimate)
                    const compute = d.training_compute_flops || 0;
                    const costPerFlop = 1e-20; // Very rough estimate
                    return compute * costPerFlop;
                });
                chartLabel = 'Estimated Training Cost (USD)';
            } else {
                values = data.map(d => d.context_window || 0);
                chartLabel = 'Context Window (tokens)';
            }
            break;

        case 'cloud':
            data = window.cloudData || getSampleCloudData();
            labels = data.map(d => `${d.provider} ${d.instance_type}`);
            if (metric === 'performance') {
                values = data.map(d => d.tflops || 0);
                chartLabel = 'TFLOPS';
            } else if (metric === 'efficiency') {
                values = data.map(d => (d.tflops || 0) / (d.on_demand_hourly || 1));
                chartLabel = 'TFLOPS per Dollar';
            } else if (metric === 'cost') {
                values = data.map(d => d.on_demand_hourly || 0);
                chartLabel = 'Cost (USD/hour)';
            } else {
                const onDemand = data.map(d => d.on_demand_hourly || 0);
                const spot = data.map(d => d.spot_hourly || 0);
                values = onDemand.map((od, i) => od > 0 ? ((od - spot[i]) / od) * 100 : 0);
                chartLabel = 'Spot Savings (%)';
            }
            break;

        default:
            console.warn('Unknown comparison type:', type);
            return;
    }

    chartInstances.comparison.data.labels = labels;
    chartInstances.comparison.data.datasets = [{
        label: chartLabel,
        data: values,
        backgroundColor: chartColors.primary,
        borderRadius: 6
    }];
    chartInstances.comparison.update();
}

/**
 * Update chart theme for dark mode
 */
function updateChartsTheme(isDark) {
    const textColor = isDark ? '#f9fafb' : '#111827';
    const gridColor = isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)';

    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;

    // Update all chart instances
    Object.values(chartInstances).forEach(chart => {
        if (chart && chart.options) {
            chart.update();
        }
    });
}

/**
 * Utility: Format large numbers
 */
function formatNumber(num) {
    if (num >= 1e12) return (num / 1e12).toFixed(1) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(1) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(1) + 'M';
    if (num >= 1e3) return (num / 1e3).toFixed(1) + 'K';
    return num.toFixed(0);
}

/**
 * Sample data generators (fallback if real data not loaded)
 */
function getSampleHardwareData() {
    return [
        { year: 1965, name: 'IBM System/360', cpu_transistors: 5000, cpu_clock_mhz: 1, ram_mb: 0.064, price_usd: 250000 },
        { year: 1971, name: 'Intel 4004', cpu_transistors: 2300, cpu_clock_mhz: 0.74, ram_mb: 0.001, price_usd: 60 },
        { year: 1978, name: 'Intel 8086', cpu_transistors: 29000, cpu_clock_mhz: 5, ram_mb: 1, price_usd: 360 },
        { year: 1993, name: 'Pentium', cpu_transistors: 3100000, cpu_clock_mhz: 60, ram_mb: 8, price_usd: 878 },
        { year: 2006, name: 'Core 2 Duo', cpu_transistors: 291000000, cpu_clock_mhz: 2400, ram_mb: 2048, price_usd: 316 },
        { year: 2017, name: 'Core i9-7980XE', cpu_transistors: 7200000000, cpu_clock_mhz: 2600, ram_mb: 131072, price_usd: 1999 },
        { year: 2024, name: 'Ryzen 9 9950X', cpu_transistors: 28600000000, cpu_clock_mhz: 4300, ram_mb: 262144, price_usd: 699 }
    ];
}

function getSampleGPUData() {
    return [
        { year: 1999, name: 'GeForce 256', manufacturer: 'NVIDIA', tflops_fp32: 0.48, vram_gb: 0.032, tdp_watts: 35 },
        { year: 2006, name: 'GeForce 8800 GTX', manufacturer: 'NVIDIA', tflops_fp32: 0.52, vram_gb: 0.768, tdp_watts: 155 },
        { year: 2016, name: 'GTX 1080', manufacturer: 'NVIDIA', tflops_fp32: 8.9, vram_gb: 8, tdp_watts: 180 },
        { year: 2020, name: 'RTX 3090', manufacturer: 'NVIDIA', tflops_fp32: 35.6, vram_gb: 24, tdp_watts: 350 },
        { year: 2022, name: 'RTX 4090', manufacturer: 'NVIDIA', tflops_fp32: 82.6, vram_gb: 24, tdp_watts: 450 },
        { year: 2020, name: 'RX 6900 XT', manufacturer: 'AMD', tflops_fp32: 23.0, vram_gb: 16, tdp_watts: 300 },
        { year: 2023, name: 'RX 7900 XTX', manufacturer: 'AMD', tflops_fp32: 61.0, vram_gb: 24, tdp_watts: 355 }
    ];
}

function getSampleLLMData() {
    return [
        { year: 2018, name: 'BERT-Base', parameters_billions: 0.11, training_compute_flops: 1e20, context_window: 512 },
        { year: 2019, name: 'GPT-2', parameters_billions: 1.5, training_compute_flops: 1e21, context_window: 1024 },
        { year: 2020, name: 'GPT-3', parameters_billions: 175, training_compute_flops: 3.14e23, context_window: 2048 },
        { year: 2022, name: 'GPT-3.5', parameters_billions: 175, training_compute_flops: 5e23, context_window: 4096 },
        { year: 2023, name: 'GPT-4', parameters_billions: 1760, training_compute_flops: 1e25, context_window: 8192 },
        { year: 2024, name: 'Claude 3.5 Sonnet', parameters_billions: 200, training_compute_flops: 1e24, context_window: 200000 }
    ];
}

function getSampleCloudData() {
    return [
        { provider: 'AWS', instance_type: 'p5.48xlarge', tflops: 8000, on_demand_hourly: 98.32, spot_hourly: 29.50, year: 2023 },
        { provider: 'AWS', instance_type: 'p4d.24xlarge', tflops: 2496, on_demand_hourly: 32.77, spot_hourly: 9.83, year: 2020 },
        { provider: 'Azure', instance_type: 'ND96asr_v4', tflops: 2496, on_demand_hourly: 27.20, spot_hourly: 8.16, year: 2021 },
        { provider: 'GCP', instance_type: 'a2-ultragpu-8g', tflops: 2496, on_demand_hourly: 33.22, spot_hourly: 9.97, year: 2021 }
    ];
}

// Make functions globally available
window.initializeCharts = initializeCharts;
window.updateGPUChartsWithFilter = updateGPUChartsWithFilter;
window.updateComparisonChartData = updateComparisonChartData;
window.updateChartsTheme = updateChartsTheme;
