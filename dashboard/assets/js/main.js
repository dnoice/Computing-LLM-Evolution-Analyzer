/**
 * Computing Evolution Dashboard - Main JavaScript
 *
 * This file handles:
 * - Alpine.js data and state management
 * - Dark mode functionality
 * - Navigation and UI interactions
 * - Cost calculator logic
 * - Data filtering
 */

// Initialize AOS (Animate On Scroll)
document.addEventListener('DOMContentLoaded', () => {
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        offset: 100
    });
});

/**
 * Main Alpine.js application
 */
function dashboardApp() {
    return {
        // State Management
        darkMode: false,
        mobileMenuOpen: false,
        gpuFilter: 'all',
        loading: true,
        loadingMessage: 'Initializing dashboard...',
        loadingProgress: 0,

        // Stats Data
        stats: {
            hardware: {
                count: 30,
                years: '1965-2024',
                span: 59
            },
            gpu: {
                count: 28,
                years: '1999-2024',
                span: 25
            },
            llm: {
                count: 22,
                years: '2018-2024',
                span: 6
            },
            cloud: {
                count: 17,
                providers: 3
            }
        },

        // CAGR Data (sample values - will be populated from real data)
        cagrData: {
            transistors: '41.2%',
            clockSpeed: '32.1%',
            cores: '24.5%',
            gpuTflops: '62.8%',
            gpuVram: '45.3%',
            llmParameters: '458.7%',
            llmCompute: '1177.6%'
        },

        // Comparison Tool State
        comparison: {
            type: 'hardware',
            metric: 'performance',
            items: []
        },

        // Cost Calculator State
        costCalc: {
            modelSize: 7,
            trainingTokens: 1000,
            useSpot: 'true',
            results: false,
            estimatedCost: 0,
            trainingDays: 0,
            bestProvider: 'AWS'
        },

        // Initialization
        init() {
            // Check for saved dark mode preference
            const savedDarkMode = localStorage.getItem('darkMode');
            if (savedDarkMode !== null) {
                this.darkMode = savedDarkMode === 'true';
            } else {
                // Check system preference
                this.darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
            }
            this.applyDarkMode();

            // Load data
            this.loadData();

            // Initialize charts after data is loaded
            setTimeout(() => {
                if (typeof initializeCharts === 'function') {
                    initializeCharts();
                }
            }, 100);

            // Watch for GPU filter changes
            this.$watch('gpuFilter', (value) => {
                this.updateGPUCharts(value);
            });

            // Watch for comparison changes
            this.$watch('comparison.type', () => {
                this.updateComparisonChart();
            });
            this.$watch('comparison.metric', () => {
                this.updateComparisonChart();
            });
        },

        // Dark Mode Functions
        toggleDarkMode() {
            this.darkMode = !this.darkMode;
            this.applyDarkMode();
            localStorage.setItem('darkMode', this.darkMode);
        },

        applyDarkMode() {
            if (this.darkMode) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }

            // Update charts if they exist
            if (typeof updateChartsTheme === 'function') {
                updateChartsTheme(this.darkMode);
            }
        },

        // Navigation Functions
        scrollToSection(sectionId) {
            const element = document.getElementById(sectionId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        },

        // Data Loading
        async loadData() {
            try {
                this.loadingMessage = 'Loading hardware data...';
                this.loadingProgress = 10;

                // Load hardware data
                const hardwareData = await loadHardwareData();
                if (hardwareData) {
                    window.hardwareData = hardwareData;
                }
                this.loadingProgress = 25;

                this.loadingMessage = 'Loading GPU data...';
                // Load GPU data
                const gpuData = await loadGPUData();
                if (gpuData) {
                    window.gpuData = gpuData;
                }
                this.loadingProgress = 40;

                this.loadingMessage = 'Loading LLM data...';
                // Load LLM data
                const llmData = await loadLLMData();
                if (llmData) {
                    window.llmData = llmData;
                }
                this.loadingProgress = 55;

                this.loadingMessage = 'Loading cloud data...';
                // Load Cloud data
                const cloudData = await loadCloudData();
                if (cloudData) {
                    window.cloudData = cloudData;
                }
                this.loadingProgress = 70;

                this.loadingMessage = 'Processing data...';
                // Update stats from loaded data
                this.updateStatsFromData();
                this.loadingProgress = 85;

                this.loadingMessage = 'Initializing charts...';
                // Small delay to show the message
                await new Promise(resolve => setTimeout(resolve, 500));
                this.loadingProgress = 100;

                // Hide loading overlay
                setTimeout(() => {
                    this.loading = false;
                }, 500);

                console.log('All data loaded successfully');
            } catch (error) {
                console.error('Error loading data:', error);
                this.showNotification('Error loading data. Using sample data.', 'warning');
                this.loading = false;
            }
        },

        // Update stats from loaded data
        updateStatsFromData() {
            if (window.hardwareData) {
                this.stats.hardware.count = window.hardwareData.length;
            }
            if (window.gpuData) {
                this.stats.gpu.count = window.gpuData.length;
            }
            if (window.llmData) {
                this.stats.llm.count = window.llmData.length;
            }
            if (window.cloudData) {
                this.stats.cloud.count = window.cloudData.length;
            }

            // Calculate real CAGR values from loaded data
            this.updateCAGRData();
        },

        // Calculate and update CAGR data from real datasets
        updateCAGRData() {
            // Hardware CAGR
            if (window.hardwareData && typeof getHardwareCAGR === 'function') {
                const hwCAGR = getHardwareCAGR(window.hardwareData);
                if (hwCAGR.transistors) {
                    this.cagrData.transistors = hwCAGR.transistors.toFixed(1) + '%';
                }
                if (hwCAGR.clockSpeed) {
                    this.cagrData.clockSpeed = hwCAGR.clockSpeed.toFixed(1) + '%';
                }
                if (hwCAGR.cores) {
                    this.cagrData.cores = hwCAGR.cores.toFixed(1) + '%';
                }
            }

            // GPU CAGR
            if (window.gpuData && typeof getGPUCAGR === 'function') {
                const gpuCAGR = getGPUCAGR(window.gpuData);
                if (gpuCAGR.tflops) {
                    this.cagrData.gpuTflops = gpuCAGR.tflops.toFixed(1) + '%';
                }
                if (gpuCAGR.vram) {
                    this.cagrData.gpuVram = gpuCAGR.vram.toFixed(1) + '%';
                }
            }

            // LLM CAGR
            if (window.llmData && typeof getLLMCAGR === 'function') {
                const llmCAGR = getLLMCAGR(window.llmData);
                if (llmCAGR.parameters) {
                    this.cagrData.llmParameters = llmCAGR.parameters.toFixed(1) + '%';
                }
                if (llmCAGR.compute) {
                    this.cagrData.llmCompute = llmCAGR.compute.toFixed(1) + '%';
                }
            }
        },

        // GPU Filter Functions
        updateGPUCharts(filter) {
            if (typeof updateGPUChartsWithFilter === 'function') {
                updateGPUChartsWithFilter(filter);
            }
        },

        // Comparison Tool Functions
        updateComparisonChart() {
            if (typeof updateComparisonChartData === 'function') {
                updateComparisonChartData(this.comparison.type, this.comparison.metric);
            }
        },

        // Cost Calculator Functions
        calculateCost() {
            const modelSize = parseFloat(this.costCalc.modelSize);
            const trainingTokens = parseFloat(this.costCalc.trainingTokens);
            const useSpot = this.costCalc.useSpot === 'true';

            // Validate inputs
            if (isNaN(modelSize) || modelSize <= 0) {
                this.showNotification('Please enter a valid model size', 'error');
                return;
            }

            if (isNaN(trainingTokens) || trainingTokens <= 0) {
                this.showNotification('Please enter valid training tokens', 'error');
                return;
            }

            // Calculate training FLOPs using Chinchilla scaling
            // Formula: 6 * N * D (N = parameters, D = tokens)
            const trainingFlops = 6 * (modelSize * 1e9) * (trainingTokens * 1e9);

            // Estimate using H100 performance (assuming 1000 TFLOPS for FP16 training)
            const h100Tflops = 1000; // TFLOPS
            const trainingSeconds = trainingFlops / (h100Tflops * 1e12);
            const trainingDays = trainingSeconds / (24 * 3600);

            // Cost estimation (AWS p5.48xlarge with 8xH100)
            const instanceTflops = 8000; // 8x H100
            const actualTrainingDays = trainingFlops / (instanceTflops * 1e12 * 24 * 3600);

            // Pricing
            const spotHourlyRate = 29.50; // AWS p5.48xlarge spot
            const onDemandHourlyRate = 98.32; // AWS p5.48xlarge on-demand

            const hourlyRate = useSpot ? spotHourlyRate : onDemandHourlyRate;
            const trainingHours = actualTrainingDays * 24;
            const totalCost = trainingHours * hourlyRate;

            // Update results
            this.costCalc.estimatedCost = Math.round(totalCost);
            this.costCalc.trainingDays = Math.round(actualTrainingDays * 10) / 10;
            this.costCalc.bestProvider = 'AWS';
            this.costCalc.results = true;

            // Show notification
            this.showNotification('Cost calculated successfully!', 'success');
        },

        // Notification System
        showNotification(message, type = 'info') {
            // Create notification element
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-xl max-w-sm transform transition-all duration-300 ${
                type === 'success' ? 'bg-green-500 text-white' :
                type === 'error' ? 'bg-red-500 text-white' :
                type === 'warning' ? 'bg-yellow-500 text-white' :
                'bg-blue-500 text-white'
            }`;

            notification.innerHTML = `
                <div class="flex items-center space-x-3">
                    <i class="fas ${
                        type === 'success' ? 'fa-check-circle' :
                        type === 'error' ? 'fa-times-circle' :
                        type === 'warning' ? 'fa-exclamation-triangle' :
                        'fa-info-circle'
                    }"></i>
                    <p>${message}</p>
                </div>
            `;

            document.body.appendChild(notification);

            // Animate in
            setTimeout(() => {
                notification.style.transform = 'translateX(0)';
                notification.style.opacity = '1';
            }, 10);

            // Remove after 3 seconds
            setTimeout(() => {
                notification.style.transform = 'translateX(100%)';
                notification.style.opacity = '0';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, 3000);
        },

        // Utility Functions
        formatNumber(num) {
            if (num >= 1e9) {
                return (num / 1e9).toFixed(1) + 'B';
            } else if (num >= 1e6) {
                return (num / 1e6).toFixed(1) + 'M';
            } else if (num >= 1e3) {
                return (num / 1e3).toFixed(1) + 'K';
            }
            return num.toString();
        },

        formatCurrency(num) {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            }).format(num);
        },

        formatPercentage(num) {
            return num.toFixed(1) + '%';
        }
    };
}

/**
 * Smooth scroll to anchor links
 */
document.addEventListener('DOMContentLoaded', () => {
    // Handle all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                e.preventDefault();
                const element = document.querySelector(href);
                if (element) {
                    element.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

/**
 * Add active state to navigation based on scroll position
 */
let ticking = false;
window.addEventListener('scroll', () => {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            updateActiveNavLink();
            ticking = false;
        });
        ticking = true;
    }
});

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    let currentSection = '';
    const scrollPosition = window.pageYOffset + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;

        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('text-primary', 'bg-primary-50');
        const href = link.getAttribute('href');
        if (href === '#' + currentSection) {
            link.classList.add('text-primary', 'bg-primary-50');
        }
    });
}

/**
 * Performance optimization: Lazy load charts when visible
 */
const chartObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const canvas = entry.target;
            const chartId = canvas.id;

            // Trigger chart initialization if not already done
            if (canvas.dataset.loaded !== 'true') {
                console.log('Loading chart:', chartId);
                canvas.dataset.loaded = 'true';

                // Dispatch custom event for chart initialization
                const event = new CustomEvent('chartVisible', {
                    detail: { chartId }
                });
                window.dispatchEvent(event);
            }
        }
    });
}, {
    rootMargin: '50px'
});

// Observe all canvas elements
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('canvas').forEach(canvas => {
        chartObserver.observe(canvas);
    });
});

/**
 * Export functionality
 */
function exportData(format = 'json') {
    const data = {
        hardware: window.hardwareData || [],
        gpu: window.gpuData || [],
        llm: window.llmData || [],
        cloud: window.cloudData || []
    };

    let content, filename, mimeType;

    switch (format) {
        case 'json':
            content = JSON.stringify(data, null, 2);
            filename = 'computing-evolution-data.json';
            mimeType = 'application/json';
            break;
        case 'csv':
            // Convert to CSV (simplified)
            content = convertToCSV(data);
            filename = 'computing-evolution-data.csv';
            mimeType = 'text/csv';
            break;
        default:
            console.error('Unsupported export format:', format);
            return;
    }

    // Create download link
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * Convert data to CSV format
 */
function convertToCSV(data) {
    let csv = '';

    // Helper function to escape CSV values
    const escapeCSV = (value) => {
        if (value === null || value === undefined) return '';
        const stringValue = String(value);
        if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
            return '"' + stringValue.replace(/"/g, '""') + '"';
        }
        return stringValue;
    };

    // Hardware section
    if (data.hardware && data.hardware.length > 0) {
        csv += 'HARDWARE SYSTEMS\n';
        const hardwareHeaders = Object.keys(data.hardware[0]);
        csv += hardwareHeaders.map(escapeCSV).join(',') + '\n';
        data.hardware.forEach(row => {
            csv += hardwareHeaders.map(header => escapeCSV(row[header])).join(',') + '\n';
        });
        csv += '\n';
    }

    // GPU section
    if (data.gpu && data.gpu.length > 0) {
        csv += 'GPU MODELS\n';
        const gpuHeaders = Object.keys(data.gpu[0]);
        csv += gpuHeaders.map(escapeCSV).join(',') + '\n';
        data.gpu.forEach(row => {
            csv += gpuHeaders.map(header => escapeCSV(row[header])).join(',') + '\n';
        });
        csv += '\n';
    }

    // LLM section
    if (data.llm && data.llm.length > 0) {
        csv += 'LLM MODELS\n';
        const llmHeaders = Object.keys(data.llm[0]);
        csv += llmHeaders.map(escapeCSV).join(',') + '\n';
        data.llm.forEach(row => {
            csv += llmHeaders.map(header => escapeCSV(row[header])).join(',') + '\n';
        });
        csv += '\n';
    }

    // Cloud section
    if (data.cloud && data.cloud.length > 0) {
        csv += 'CLOUD INSTANCES\n';
        const cloudHeaders = Object.keys(data.cloud[0]);
        csv += cloudHeaders.map(escapeCSV).join(',') + '\n';
        data.cloud.forEach(row => {
            csv += cloudHeaders.map(header => escapeCSV(row[header])).join(',') + '\n';
        });
        csv += '\n';
    }

    return csv;
}

// Make export function globally available
window.exportData = exportData;
