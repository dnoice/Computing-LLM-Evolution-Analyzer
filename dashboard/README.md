# Computing Evolution Dashboard

A beautiful, interactive web dashboard for analyzing the evolution of computing hardware, GPUs, Large Language Models, and cloud infrastructure.

## Features

### Comprehensive Data Visualization
- **Moore's Law Analysis**: Track transistor density evolution with predictive modeling
- **Hardware Evolution**: Analyze 59 years of CPU advancement (1965-2024)
- **GPU Performance**: Compare 28 GPUs from NVIDIA, AMD, and Intel (1999-2024)
- **LLM Scaling**: Track 22 language models from BERT to GPT-4 (2018-2024)
- **Cloud Economics**: Compare AWS, Azure, and GCP pricing and performance

### Modern UI/UX
- **Mobile-First Design**: Fully responsive across all devices
- **Dark Mode**: Automatic theme switching with persistent preference
- **Beautiful Animations**: Smooth transitions and scroll animations
- **Interactive Charts**: Powered by Chart.js with hover tooltips
- **Filtering & Comparison**: Dynamic data filtering and side-by-side comparisons

### Technology Stack
- **Tailwind CSS**: Utility-first CSS framework
- **Alpine.js**: Lightweight reactive framework
- **Chart.js**: Beautiful interactive charts
- **Font Awesome**: Comprehensive icon library
- **AOS**: Animate on scroll library

## Quick Start

### 1. Using Python Server (Recommended)

```bash
# Navigate to dashboard directory
cd dashboard

# Start the development server
python serve.py

# Or specify a custom port
python serve.py 3000
```

Then open your browser to: `http://localhost:8000`

### 2. Using Any HTTP Server

```bash
# Using Python's built-in server
python -m http.server 8000

# Using Node.js http-server
npx http-server -p 8000

# Using PHP
php -S localhost:8000
```

### 3. Direct File Access

Simply open `index.html` in your browser. However, data loading may be restricted due to CORS policies. Using a local server is recommended.

## Project Structure

```
dashboard/
├── index.html                  # Main dashboard page
├── serve.py                    # Development server script
├── README.md                   # This file
├── assets/
│   ├── css/
│   │   └── custom.css         # Custom styles with CSS variables
│   ├── js/
│   │   ├── main.js            # Alpine.js app and interactions
│   │   ├── charts.js          # Chart.js configurations
│   │   └── data-loader.js     # Data loading utilities
│   └── images/                # SVG components and images
└── data/                       # Symlink or copy of ../data/
```

## Features in Detail

### 1. Overview Dashboard
- Quick stats cards showing dataset coverage
- Dataset metadata (years, counts, providers)
- Interactive navigation to specific sections

### 2. Moore's Law Analysis
- Historical transistor count tracking
- Predictive modeling with realistic slowdown
- CAGR calculations for key metrics
- Confidence indicators for predictions

### 3. Hardware Evolution
- Transistor count evolution (log scale)
- Clock speed trends
- RAM capacity growth
- Price vs performance analysis

### 4. GPU Performance
- Compute performance (TFLOPS) evolution
- VRAM capacity trends
- Power efficiency analysis (TFLOPS/Watt)
- Manufacturer comparison (NVIDIA, AMD, Intel)
- Interactive filtering by manufacturer

### 5. LLM Analysis
- Parameter scaling visualization
- Training compute evolution
- Context window growth
- Capability radar charts
- Reality check warnings for unsustainable growth

### 6. Cloud Cost Analysis
- Interactive cost calculator
- Provider comparison (AWS, Azure, GCP)
- Spot instance savings analysis
- Cost efficiency rankings
- Instance type comparisons

### 7. Comparison Tool
- Side-by-side comparisons
- Multiple comparison metrics
- Customizable visualizations
- Export capabilities

## Customization

### CSS Variables

All colors, spacing, and typography are defined in CSS custom properties in `assets/css/custom.css`:

```css
:root {
    --color-primary: #3b82f6;
    --color-secondary: #8b5cf6;
    --spacing-md: 1rem;
    --font-size-base: 1rem;
    /* ... and many more */
}
```

### Dark Mode

The dashboard automatically detects system dark mode preference and saves user preference in localStorage. Colors are managed through CSS custom properties:

```css
.dark {
    --color-bg-primary: #111827;
    --color-text-primary: #f9fafb;
    /* ... */
}
```

### Chart Themes

Charts automatically update when toggling dark mode. Chart colors are defined in `charts.js`:

```javascript
const chartColors = {
    primary: '#3b82f6',
    secondary: '#8b5cf6',
    // ...
};
```

## Data Integration

The dashboard loads data from JSON files in the `../data/` directory. It expects the following structure:

### Hardware Data (`../data/hardware/systems.json`)
```json
[
    {
        "year": 2024,
        "name": "System Name",
        "cpu_transistors": 28600000000,
        "cpu_clock_mhz": 4300,
        "ram_mb": 262144,
        "cpu_cores": 16,
        "price_usd": 699
    }
]
```

### GPU Data (`../data/gpu/gpus.json`)
```json
[
    {
        "year": 2022,
        "name": "GPU Name",
        "manufacturer": "NVIDIA",
        "tflops_fp32": 82.6,
        "vram_gb": 24,
        "tdp_watts": 450
    }
]
```

### LLM Data (`../data/llm/models.json`)
```json
[
    {
        "year": 2024,
        "name": "Model Name",
        "parameters_billions": 200,
        "training_compute_flops": 1e24,
        "context_window": 200000
    }
]
```

### Cloud Data (`../data/cloud/instances.json`)
```json
[
    {
        "provider": "AWS",
        "instance_type": "p5.48xlarge",
        "gpu_count": 8,
        "tflops": 8000,
        "on_demand_hourly": 98.32,
        "spot_hourly": 29.50
    }
]
```

## Performance Optimization

### Lazy Loading
Charts are lazy-loaded as they become visible in the viewport using Intersection Observer API.

### Caching
Data is cached in memory after initial load to prevent redundant fetches.

### Throttling
Scroll events are throttled using `requestAnimationFrame` for optimal performance.

### Responsive Images
All visual assets are optimized for different screen sizes.

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: iOS Safari, Chrome Mobile

**Minimum Requirements:**
- ES6 support
- CSS Grid & Flexbox
- CSS Custom Properties
- Fetch API

## Development

### Adding New Charts

1. Add canvas element to `index.html`:
```html
<canvas id="myNewChart"></canvas>
```

2. Create chart in `assets/js/charts.js`:
```javascript
function initializeMyNewChart() {
    const ctx = document.getElementById('myNewChart');
    chartInstances.myNewChart = new Chart(ctx, {
        // Chart configuration
    });
}
```

3. Call initialization function:
```javascript
function initializeCharts() {
    // ... existing charts
    initializeMyNewChart();
}
```

### Adding New Data Sources

1. Create loader function in `assets/js/data-loader.js`:
```javascript
async function loadMyNewData() {
    const response = await fetch('path/to/data.json');
    return await response.json();
}
```

2. Add to `loadAllData()` function
3. Update chart configurations to use new data

### Styling Customization

1. Update CSS variables in `assets/css/custom.css`
2. Add new utility classes following Tailwind conventions
3. Maintain mobile-first approach

## Accessibility

- Semantic HTML structure
- ARIA labels on interactive elements
- Keyboard navigation support
- Focus indicators
- Reduced motion support for users who prefer it
- Color contrast ratios meet WCAG AA standards

## Export & Sharing

### Export Data
Click the export button in the footer to download data as:
- JSON: Structured data format
- CSV: Spreadsheet-compatible format

### Share Analysis
Use browser's built-in screenshot or print functionality to share specific charts and insights.

## Troubleshooting

### Charts not loading
- Ensure you're using a local server (not file://)
- Check browser console for errors
- Verify data files are accessible

### Dark mode not persisting
- Check if localStorage is enabled
- Clear browser cache and reload

### Performance issues
- Reduce animation duration in AOS init
- Disable chart animations in defaultChartOptions
- Use production builds of CDN libraries

## Contributing

Contributions are welcome! Areas for improvement:
- Additional chart types and visualizations
- More interactive filters and controls
- Enhanced mobile experience
- Additional data sources
- Performance optimizations
- Accessibility improvements

## License

MIT License - See main project LICENSE file

## Credits

Built with:
- [Tailwind CSS](https://tailwindcss.com/)
- [Chart.js](https://www.chartjs.org/)
- [Alpine.js](https://alpinejs.dev/)
- [Font Awesome](https://fontawesome.com/)
- [AOS](https://michalsnik.github.io/aos/)

Data sources documented in `../data/SOURCES.md`

## Version

Dashboard Version: 1.0.0
Data Version: 2.1.0
Last Updated: 2024-10-30
