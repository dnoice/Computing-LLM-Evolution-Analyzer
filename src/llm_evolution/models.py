"""Data models for hardware and LLM metrics."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class HardwareMetrics:
    """Hardware system metrics and specifications."""

    name: str
    year: int
    manufacturer: str

    # CPU Metrics
    cpu_name: str
    cpu_cores: int
    cpu_transistors: int  # Number of transistors
    cpu_clock_mhz: float
    cpu_process_nm: int  # Process node in nanometers

    # Memory
    ram_mb: int

    # Storage
    storage_mb: int

    # Performance
    performance_mips: Optional[float] = None  # Millions of Instructions Per Second
    performance_flops: Optional[float] = None  # Floating Point Operations Per Second

    # Power & Economics
    power_watts: float = 0.0
    price_usd: float = 0.0

    # Architecture
    architecture: str = ""
    instruction_set: str = ""

    # Additional metadata
    notes: str = ""

    def compute_efficiency_metrics(self) -> Dict[str, float]:
        """Compute derived efficiency metrics."""
        metrics = {}

        if self.performance_mips and self.power_watts > 0:
            metrics['mips_per_watt'] = self.performance_mips / self.power_watts

        if self.performance_mips and self.price_usd > 0:
            metrics['mips_per_dollar'] = self.performance_mips / self.price_usd

        if self.cpu_transistors and self.cpu_process_nm > 0:
            metrics['transistor_density'] = self.cpu_transistors / (self.cpu_process_nm ** 2)

        return metrics

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'year': self.year,
            'manufacturer': self.manufacturer,
            'cpu_name': self.cpu_name,
            'cpu_cores': self.cpu_cores,
            'cpu_transistors': self.cpu_transistors,
            'cpu_clock_mhz': self.cpu_clock_mhz,
            'cpu_process_nm': self.cpu_process_nm,
            'ram_mb': self.ram_mb,
            'storage_mb': self.storage_mb,
            'performance_mips': self.performance_mips,
            'performance_flops': self.performance_flops,
            'power_watts': self.power_watts,
            'price_usd': self.price_usd,
            'architecture': self.architecture,
            'instruction_set': self.instruction_set,
            'notes': self.notes,
            **self.compute_efficiency_metrics()
        }


@dataclass
class LLMMetrics:
    """Large Language Model metrics and capabilities."""

    name: str
    year: int
    organization: str

    # Model Architecture
    parameters_billions: float
    architecture_type: str  # e.g., "Transformer", "GPT", "BERT"

    # Training
    training_tokens_billions: Optional[float] = None
    training_compute_flops: Optional[float] = None  # Total FLOPs for training
    training_days: Optional[int] = None

    # Capabilities
    context_window: int = 2048
    max_output_tokens: Optional[int] = None

    # Performance Scores (0-100)
    capability_score_reasoning: float = 0.0
    capability_score_coding: float = 0.0
    capability_score_math: float = 0.0
    capability_score_knowledge: float = 0.0
    capability_score_multilingual: float = 0.0

    # Economics
    cost_per_1m_input_tokens: float = 0.0
    cost_per_1m_output_tokens: float = 0.0

    # Technical Details
    num_layers: Optional[int] = None
    hidden_size: Optional[int] = None
    attention_heads: Optional[int] = None

    # Metadata
    release_date: Optional[str] = None
    model_type: str = "text"  # text, multimodal, code, etc.
    open_source: bool = False
    notes: str = ""

    def compute_scaling_metrics(self) -> Dict[str, float]:
        """Compute scaling law metrics."""
        metrics = {}

        # Chinchilla optimal compute
        if self.parameters_billions and self.training_tokens_billions:
            # Chinchilla suggests ~20 tokens per parameter
            optimal_tokens = self.parameters_billions * 20
            metrics['chinchilla_optimal_tokens'] = optimal_tokens
            metrics['chinchilla_efficiency'] = min(
                self.training_tokens_billions / optimal_tokens,
                optimal_tokens / self.training_tokens_billions
            )

        # Memory requirements (rough estimate)
        # ~4 bytes per parameter for FP32, ~2 for FP16
        if self.parameters_billions:
            metrics['memory_gb_fp32'] = self.parameters_billions * 4
            metrics['memory_gb_fp16'] = self.parameters_billions * 2

        # Compute efficiency
        if self.training_compute_flops and self.training_days:
            metrics['flops_per_day'] = self.training_compute_flops / self.training_days

        # Average capability score
        capability_scores = [
            self.capability_score_reasoning,
            self.capability_score_coding,
            self.capability_score_math,
            self.capability_score_knowledge,
            self.capability_score_multilingual
        ]
        metrics['avg_capability_score'] = sum(capability_scores) / len(capability_scores)

        return metrics

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'year': self.year,
            'organization': self.organization,
            'parameters_billions': self.parameters_billions,
            'architecture_type': self.architecture_type,
            'training_tokens_billions': self.training_tokens_billions,
            'training_compute_flops': self.training_compute_flops,
            'training_days': self.training_days,
            'context_window': self.context_window,
            'max_output_tokens': self.max_output_tokens,
            'capability_score_reasoning': self.capability_score_reasoning,
            'capability_score_coding': self.capability_score_coding,
            'capability_score_math': self.capability_score_math,
            'capability_score_knowledge': self.capability_score_knowledge,
            'capability_score_multilingual': self.capability_score_multilingual,
            'cost_per_1m_input_tokens': self.cost_per_1m_input_tokens,
            'cost_per_1m_output_tokens': self.cost_per_1m_output_tokens,
            'num_layers': self.num_layers,
            'hidden_size': self.hidden_size,
            'attention_heads': self.attention_heads,
            'release_date': self.release_date,
            'model_type': self.model_type,
            'open_source': self.open_source,
            'notes': self.notes,
            **self.compute_scaling_metrics()
        }


@dataclass
class ComparisonResult:
    """Results from comparing hardware or LLM metrics over time."""

    metric_name: str
    start_value: float
    end_value: float
    start_year: int
    end_year: int

    # Growth metrics
    absolute_growth: float = 0.0
    growth_factor: float = 0.0
    cagr_percent: float = 0.0  # Compound Annual Growth Rate

    # Moore's Law comparison (for hardware)
    moores_law_predicted: Optional[float] = None
    moores_law_accuracy: Optional[float] = None

    def __post_init__(self):
        """Calculate derived metrics."""
        self.absolute_growth = self.end_value - self.start_value

        if self.start_value > 0:
            self.growth_factor = self.end_value / self.start_value

        # Calculate CAGR
        years = self.end_year - self.start_year
        if years > 0 and self.start_value > 0:
            self.cagr_percent = (
                ((self.end_value / self.start_value) ** (1 / years) - 1) * 100
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'metric_name': self.metric_name,
            'start_value': self.start_value,
            'end_value': self.end_value,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'absolute_growth': self.absolute_growth,
            'growth_factor': self.growth_factor,
            'cagr_percent': self.cagr_percent,
            'moores_law_predicted': self.moores_law_predicted,
            'moores_law_accuracy': self.moores_law_accuracy
        }


@dataclass
class GPUMetrics:
    """GPU (Graphics Processing Unit) metrics and specifications."""

    name: str
    year: int
    manufacturer: str
    series: str  # e.g., "GeForce RTX", "Radeon RX", "Arc"

    # Core Architecture
    architecture: str  # e.g., "Ada Lovelace", "RDNA 3", "Alchemist"
    process_nm: int  # Process node in nanometers
    transistors_millions: int  # Number of transistors in millions
    die_size_mm2: float  # Die size in square millimeters

    # Compute Units
    cuda_cores: Optional[int] = None  # NVIDIA CUDA cores
    stream_processors: Optional[int] = None  # AMD stream processors
    execution_units: Optional[int] = None  # Intel execution units
    tensor_cores: Optional[int] = None  # Tensor cores for AI/ML
    rt_cores: Optional[int] = None  # Ray tracing cores

    # Clock Speeds (MHz)
    base_clock_mhz: float = 0.0
    boost_clock_mhz: float = 0.0

    # Memory
    vram_mb: int = 0  # Video RAM in MB
    memory_type: str = ""  # e.g., "GDDR6", "GDDR6X", "HBM2"
    memory_bus_width: int = 0  # Memory bus width in bits
    memory_bandwidth_gbps: float = 0.0  # Memory bandwidth in GB/s
    memory_clock_mhz: float = 0.0

    # Performance
    tflops_fp32: float = 0.0  # Single precision TFLOPS
    tflops_fp16: float = 0.0  # Half precision TFLOPS
    tflops_int8: float = 0.0  # INT8 TOPS for AI
    ray_tracing_tflops: Optional[float] = None  # RT performance

    # Power & Thermals
    tdp_watts: int = 0  # Thermal Design Power
    power_connectors: str = ""  # e.g., "8-pin + 8-pin"

    # Economics
    launch_price_usd: float = 0.0
    price_per_tflop: Optional[float] = None

    # Capabilities
    directx_version: str = ""  # e.g., "12 Ultimate"
    opengl_version: str = ""
    vulkan_support: bool = False
    ray_tracing_support: bool = False
    dlss_support: bool = False  # NVIDIA DLSS
    fsr_support: bool = False  # AMD FSR
    xess_support: bool = False  # Intel XeSS

    # Display
    max_displays: int = 0
    max_resolution: str = ""  # e.g., "8K @ 60Hz"

    # Additional metadata
    release_date: Optional[str] = None
    notes: str = ""

    def compute_efficiency_metrics(self) -> Dict[str, float]:
        """Compute derived efficiency metrics."""
        metrics = {}

        # Compute cores (unified metric)
        total_cores = 0
        if self.cuda_cores:
            total_cores = self.cuda_cores
        elif self.stream_processors:
            total_cores = self.stream_processors
        elif self.execution_units:
            total_cores = self.execution_units
        metrics['total_compute_cores'] = total_cores

        # Performance per watt
        if self.tflops_fp32 > 0 and self.tdp_watts > 0:
            metrics['tflops_per_watt'] = self.tflops_fp32 / self.tdp_watts

        # Performance per dollar
        if self.tflops_fp32 > 0 and self.launch_price_usd > 0:
            metrics['tflops_per_dollar'] = self.tflops_fp32 / self.launch_price_usd
            self.price_per_tflop = self.launch_price_usd / self.tflops_fp32
            metrics['price_per_tflop'] = self.price_per_tflop

        # Memory bandwidth per core
        if total_cores > 0 and self.memory_bandwidth_gbps > 0:
            metrics['bandwidth_per_core_mbps'] = (self.memory_bandwidth_gbps * 1000) / total_cores

        # Transistor density
        if self.transistors_millions > 0 and self.die_size_mm2 > 0:
            metrics['transistor_density_per_mm2'] = (self.transistors_millions * 1_000_000) / self.die_size_mm2

        # Performance density
        if self.tflops_fp32 > 0 and self.die_size_mm2 > 0:
            metrics['tflops_per_mm2'] = self.tflops_fp32 / self.die_size_mm2

        return metrics

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        base_dict = {
            'name': self.name,
            'year': self.year,
            'manufacturer': self.manufacturer,
            'series': self.series,
            'architecture': self.architecture,
            'process_nm': self.process_nm,
            'transistors_millions': self.transistors_millions,
            'die_size_mm2': self.die_size_mm2,
            'cuda_cores': self.cuda_cores,
            'stream_processors': self.stream_processors,
            'execution_units': self.execution_units,
            'tensor_cores': self.tensor_cores,
            'rt_cores': self.rt_cores,
            'base_clock_mhz': self.base_clock_mhz,
            'boost_clock_mhz': self.boost_clock_mhz,
            'vram_mb': self.vram_mb,
            'memory_type': self.memory_type,
            'memory_bus_width': self.memory_bus_width,
            'memory_bandwidth_gbps': self.memory_bandwidth_gbps,
            'memory_clock_mhz': self.memory_clock_mhz,
            'tflops_fp32': self.tflops_fp32,
            'tflops_fp16': self.tflops_fp16,
            'tflops_int8': self.tflops_int8,
            'ray_tracing_tflops': self.ray_tracing_tflops,
            'tdp_watts': self.tdp_watts,
            'power_connectors': self.power_connectors,
            'launch_price_usd': self.launch_price_usd,
            'price_per_tflop': self.price_per_tflop,
            'directx_version': self.directx_version,
            'opengl_version': self.opengl_version,
            'vulkan_support': self.vulkan_support,
            'ray_tracing_support': self.ray_tracing_support,
            'dlss_support': self.dlss_support,
            'fsr_support': self.fsr_support,
            'xess_support': self.xess_support,
            'max_displays': self.max_displays,
            'max_resolution': self.max_resolution,
            'release_date': self.release_date,
            'notes': self.notes,
        }

        # Add computed efficiency metrics
        base_dict.update(self.compute_efficiency_metrics())

        return base_dict
