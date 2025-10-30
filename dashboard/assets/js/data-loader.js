/**
 * Computing Evolution Dashboard - Data Loader
 *
 * This file handles loading data from JSON files:
 * - Hardware systems data
 * - GPU data
 * - LLM models data
 * - Cloud instances data
 */

// Base path for data files (adjust based on your directory structure)
const DATA_BASE_PATH = '../data';

/**
 * Load Hardware Systems Data
 */
async function loadHardwareData() {
    try {
        const response = await fetch(`${DATA_BASE_PATH}/hardware/systems.json`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Hardware data loaded:', data.length, 'systems');
        return data;
    } catch (error) {
        console.error('Error loading hardware data:', error);
        console.log('Using sample hardware data');
        return getSampleHardwareData();
    }
}

/**
 * Load GPU Data
 */
async function loadGPUData() {
    try {
        const response = await fetch(`${DATA_BASE_PATH}/gpu/gpus.json`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('GPU data loaded:', data.length, 'GPUs');
        return data;
    } catch (error) {
        console.error('Error loading GPU data:', error);
        console.log('Using sample GPU data');
        return getSampleGPUData();
    }
}

/**
 * Load LLM Models Data
 */
async function loadLLMData() {
    try {
        const response = await fetch(`${DATA_BASE_PATH}/llm/models.json`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('LLM data loaded:', data.length, 'models');
        return data;
    } catch (error) {
        console.error('Error loading LLM data:', error);
        console.log('Using sample LLM data');
        return getSampleLLMData();
    }
}

/**
 * Load Cloud Instances Data
 */
async function loadCloudData() {
    try {
        const response = await fetch(`${DATA_BASE_PATH}/cloud/instances.json`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Cloud data loaded:', data.length, 'instances');
        return data;
    } catch (error) {
        console.error('Error loading cloud data:', error);
        console.log('Using sample cloud data');
        return getSampleCloudData();
    }
}

/**
 * Load all data at once
 */
async function loadAllData() {
    const results = await Promise.allSettled([
        loadHardwareData(),
        loadGPUData(),
        loadLLMData(),
        loadCloudData()
    ]);

    return {
        hardware: results[0].status === 'fulfilled' ? results[0].value : [],
        gpu: results[1].status === 'fulfilled' ? results[1].value : [],
        llm: results[2].status === 'fulfilled' ? results[2].value : [],
        cloud: results[3].status === 'fulfilled' ? results[3].value : []
    };
}

/**
 * Calculate CAGR (Compound Annual Growth Rate)
 */
function calculateCAGR(startValue, endValue, years) {
    if (startValue <= 0 || endValue <= 0 || years <= 0) {
        return 0;
    }
    return (Math.pow(endValue / startValue, 1 / years) - 1) * 100;
}

/**
 * Get CAGR for all hardware metrics
 */
function getHardwareCAGR(data) {
    if (!data || data.length < 2) {
        return {};
    }

    const sorted = [...data].sort((a, b) => a.year - b.year);
    const first = sorted[0];
    const last = sorted[sorted.length - 1];
    const years = last.year - first.year;

    return {
        transistors: calculateCAGR(first.cpu_transistors || 1, last.cpu_transistors || 1, years),
        clockSpeed: calculateCAGR(first.cpu_clock_mhz || 1, last.cpu_clock_mhz || 1, years),
        ram: calculateCAGR(first.ram_mb || 1, last.ram_mb || 1, years),
        cores: calculateCAGR(first.cpu_cores || 1, last.cpu_cores || 1, years)
    };
}

/**
 * Get CAGR for GPU metrics
 */
function getGPUCAGR(data) {
    if (!data || data.length < 2) {
        return {};
    }

    const sorted = [...data].sort((a, b) => a.year - b.year);
    const first = sorted[0];
    const last = sorted[sorted.length - 1];
    const years = last.year - first.year;

    return {
        tflops: calculateCAGR(first.tflops_fp32 || 1, last.tflops_fp32 || 1, years),
        vram: calculateCAGR(first.vram_gb || 1, last.vram_gb || 1, years),
        memoryBandwidth: calculateCAGR(first.memory_bandwidth_gbps || 1, last.memory_bandwidth_gbps || 1, years),
        efficiency: calculateCAGR(
            (first.tflops_fp32 || 1) / (first.tdp_watts || 1),
            (last.tflops_fp32 || 1) / (last.tdp_watts || 1),
            years
        )
    };
}

/**
 * Get CAGR for LLM metrics
 */
function getLLMCAGR(data) {
    if (!data || data.length < 2) {
        return {};
    }

    const sorted = [...data].sort((a, b) => a.year - b.year);
    const first = sorted[0];
    const last = sorted[sorted.length - 1];
    const years = last.year - first.year;

    return {
        parameters: calculateCAGR(first.parameters_billions || 1, last.parameters_billions || 1, years),
        compute: calculateCAGR(first.training_compute_flops || 1, last.training_compute_flops || 1, years),
        contextWindow: calculateCAGR(first.context_window || 1, last.context_window || 1, years)
    };
}

/**
 * Get statistics for a dataset
 */
function getDatasetStats(data, field) {
    if (!data || data.length === 0) {
        return { min: 0, max: 0, avg: 0, median: 0 };
    }

    const values = data.map(d => d[field] || 0).filter(v => v > 0);
    if (values.length === 0) {
        return { min: 0, max: 0, avg: 0, median: 0 };
    }

    const sorted = [...values].sort((a, b) => a - b);
    const sum = values.reduce((acc, v) => acc + v, 0);

    return {
        min: sorted[0],
        max: sorted[sorted.length - 1],
        avg: sum / values.length,
        median: sorted[Math.floor(sorted.length / 2)]
    };
}

/**
 * Filter data by year range
 */
function filterByYearRange(data, startYear, endYear) {
    return data.filter(d => d.year >= startYear && d.year <= endYear);
}

/**
 * Filter data by manufacturer/provider
 */
function filterByManufacturer(data, manufacturer) {
    return data.filter(d =>
        d.manufacturer?.toLowerCase() === manufacturer.toLowerCase() ||
        d.provider?.toLowerCase() === manufacturer.toLowerCase()
    );
}

/**
 * Get unique manufacturers/providers from data
 */
function getUniqueManufacturers(data) {
    const manufacturers = new Set();
    data.forEach(d => {
        if (d.manufacturer) manufacturers.add(d.manufacturer);
        if (d.provider) manufacturers.add(d.provider);
    });
    return Array.from(manufacturers);
}

/**
 * Sort data by field
 */
function sortByField(data, field, ascending = true) {
    const sorted = [...data].sort((a, b) => {
        const aVal = a[field] || 0;
        const bVal = b[field] || 0;
        return ascending ? aVal - bVal : bVal - aVal;
    });
    return sorted;
}

/**
 * Get top N items by field
 */
function getTopN(data, field, n = 10) {
    return sortByField(data, field, false).slice(0, n);
}

/**
 * Calculate growth factor between two values
 */
function calculateGrowthFactor(startValue, endValue) {
    if (startValue <= 0) return 0;
    return endValue / startValue;
}

/**
 * Format large numbers for display
 */
function formatNumber(num, decimals = 1) {
    if (num >= 1e12) return (num / 1e12).toFixed(decimals) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(decimals) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(decimals) + 'M';
    if (num >= 1e3) return (num / 1e3).toFixed(decimals) + 'K';
    return num.toFixed(decimals);
}

/**
 * Format currency
 */
function formatCurrency(num) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(num);
}

/**
 * Format percentage
 */
function formatPercentage(num, decimals = 1) {
    return num.toFixed(decimals) + '%';
}

/**
 * Sample data fallbacks (same as in charts.js)
 */
function getSampleHardwareData() {
    return [
        { year: 1965, name: 'IBM System/360', cpu_transistors: 5000, cpu_clock_mhz: 1, ram_mb: 0.064, cpu_cores: 1, price_usd: 250000 },
        { year: 1971, name: 'Intel 4004', cpu_transistors: 2300, cpu_clock_mhz: 0.74, ram_mb: 0.001, cpu_cores: 1, price_usd: 60 },
        { year: 1978, name: 'Intel 8086', cpu_transistors: 29000, cpu_clock_mhz: 5, ram_mb: 1, cpu_cores: 1, price_usd: 360 },
        { year: 1993, name: 'Pentium', cpu_transistors: 3100000, cpu_clock_mhz: 60, ram_mb: 8, cpu_cores: 1, price_usd: 878 },
        { year: 2006, name: 'Core 2 Duo', cpu_transistors: 291000000, cpu_clock_mhz: 2400, ram_mb: 2048, cpu_cores: 2, price_usd: 316 },
        { year: 2017, name: 'Core i9-7980XE', cpu_transistors: 7200000000, cpu_clock_mhz: 2600, ram_mb: 131072, cpu_cores: 18, price_usd: 1999 },
        { year: 2024, name: 'Ryzen 9 9950X', cpu_transistors: 28600000000, cpu_clock_mhz: 4300, ram_mb: 262144, cpu_cores: 16, price_usd: 699 }
    ];
}

function getSampleGPUData() {
    return [
        { year: 1999, name: 'GeForce 256', manufacturer: 'NVIDIA', tflops_fp32: 0.0048, vram_gb: 0.032, tdp_watts: 35, memory_bandwidth_gbps: 2.7 },
        { year: 2006, name: 'GeForce 8800 GTX', manufacturer: 'NVIDIA', tflops_fp32: 0.52, vram_gb: 0.768, tdp_watts: 155, memory_bandwidth_gbps: 86.4 },
        { year: 2016, name: 'GTX 1080', manufacturer: 'NVIDIA', tflops_fp32: 8.9, vram_gb: 8, tdp_watts: 180, memory_bandwidth_gbps: 320 },
        { year: 2020, name: 'RTX 3090', manufacturer: 'NVIDIA', tflops_fp32: 35.6, vram_gb: 24, tdp_watts: 350, memory_bandwidth_gbps: 936 },
        { year: 2022, name: 'RTX 4090', manufacturer: 'NVIDIA', tflops_fp32: 82.6, vram_gb: 24, tdp_watts: 450, memory_bandwidth_gbps: 1008 },
        { year: 2020, name: 'RX 6900 XT', manufacturer: 'AMD', tflops_fp32: 23.0, vram_gb: 16, tdp_watts: 300, memory_bandwidth_gbps: 512 },
        { year: 2023, name: 'RX 7900 XTX', manufacturer: 'AMD', tflops_fp32: 61.0, vram_gb: 24, tdp_watts: 355, memory_bandwidth_gbps: 960 }
    ];
}

function getSampleLLMData() {
    return [
        { year: 2018, name: 'BERT-Base', parameters_billions: 0.11, training_compute_flops: 1e20, context_window: 512, organization: 'Google' },
        { year: 2019, name: 'GPT-2', parameters_billions: 1.5, training_compute_flops: 1e21, context_window: 1024, organization: 'OpenAI' },
        { year: 2020, name: 'GPT-3', parameters_billions: 175, training_compute_flops: 3.14e23, context_window: 2048, organization: 'OpenAI' },
        { year: 2022, name: 'GPT-3.5', parameters_billions: 175, training_compute_flops: 5e23, context_window: 4096, organization: 'OpenAI' },
        { year: 2023, name: 'GPT-4', parameters_billions: 1760, training_compute_flops: 1e25, context_window: 8192, organization: 'OpenAI' },
        { year: 2024, name: 'Claude 3.5 Sonnet', parameters_billions: 200, training_compute_flops: 1e24, context_window: 200000, organization: 'Anthropic' }
    ];
}

function getSampleCloudData() {
    return [
        { provider: 'AWS', instance_type: 'p5.48xlarge', gpu_model: 'H100', gpu_count: 8, tflops: 8000, on_demand_hourly: 98.32, spot_hourly: 29.50, year: 2023 },
        { provider: 'AWS', instance_type: 'p4d.24xlarge', gpu_model: 'A100', gpu_count: 8, tflops: 2496, on_demand_hourly: 32.77, spot_hourly: 9.83, year: 2020 },
        { provider: 'Azure', instance_type: 'ND96asr_v4', gpu_model: 'A100', gpu_count: 8, tflops: 2496, on_demand_hourly: 27.20, spot_hourly: 8.16, year: 2021 },
        { provider: 'GCP', instance_type: 'a2-ultragpu-8g', gpu_model: 'A100', gpu_count: 8, tflops: 2496, on_demand_hourly: 33.22, spot_hourly: 9.97, year: 2021 }
    ];
}

// Make functions globally available
window.loadHardwareData = loadHardwareData;
window.loadGPUData = loadGPUData;
window.loadLLMData = loadLLMData;
window.loadCloudData = loadCloudData;
window.loadAllData = loadAllData;
window.calculateCAGR = calculateCAGR;
window.getHardwareCAGR = getHardwareCAGR;
window.getGPUCAGR = getGPUCAGR;
window.getLLMCAGR = getLLMCAGR;
window.getDatasetStats = getDatasetStats;
window.filterByYearRange = filterByYearRange;
window.filterByManufacturer = filterByManufacturer;
window.getUniqueManufacturers = getUniqueManufacturers;
window.sortByField = sortByField;
window.getTopN = getTopN;
window.calculateGrowthFactor = calculateGrowthFactor;
window.formatNumber = formatNumber;
window.formatCurrency = formatCurrency;
window.formatPercentage = formatPercentage;
