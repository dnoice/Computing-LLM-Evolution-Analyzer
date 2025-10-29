"""Cloud cost analysis module for ML workloads."""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import math

from .models import CloudInstance, ComparisonResult


class CloudCostAnalyzer:
    """Analyzer for cloud computing costs and ML workload optimization."""

    def __init__(self, data_path: Optional[Path] = None):
        """Initialize cloud cost analyzer.

        Args:
            data_path: Path to cloud instances JSON file
        """
        if data_path is None:
            # Default to data/cloud/instances.json
            data_path = Path(__file__).parent.parent.parent / "data" / "cloud" / "instances.json"

        self.data_path = data_path
        self.instances: List[CloudInstance] = []
        self.load_data()

    def load_data(self) -> None:
        """Load cloud instance data from JSON file.

        Raises:
            FileNotFoundError: If data file doesn't exist
            json.JSONDecodeError: If JSON is malformed
            ValueError: If instance data is invalid
        """
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Cloud instance data file not found: {self.data_path}. "
                f"Please ensure data/cloud/instances.json exists."
            )
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {self.data_path}: {e.msg}",
                e.doc,
                e.pos
            )

        if not isinstance(data, list):
            raise ValueError(f"Expected list of instances, got {type(data).__name__}")

        if not data:
            raise ValueError("Cloud instance data file is empty")

        self.instances = []
        errors = []

        for idx, item in enumerate(data):
            try:
                instance = CloudInstance(**item)
                self.instances.append(instance)
            except (TypeError, ValueError) as e:
                errors.append(f"Instance {idx} ({item.get('instance_type', 'unknown')}): {str(e)}")

        if errors:
            error_msg = "Errors loading cloud instances:\n" + "\n".join(errors)
            raise ValueError(error_msg)

        if not self.instances:
            raise ValueError("No valid instances loaded from data file")

        # Sort by provider, then by price
        self.instances.sort(key=lambda x: (x.provider, x.price_ondemand_hourly))

    def get_instances_by_provider(self, provider: str) -> List[CloudInstance]:
        """Get all instances from a specific provider."""
        return [i for i in self.instances if i.provider.lower() == provider.lower()]

    def get_instance_by_type(self, instance_type: str) -> Optional[CloudInstance]:
        """Get a specific instance by type name."""
        for instance in self.instances:
            if instance.instance_type.lower() == instance_type.lower():
                return instance
        return None

    def get_instances_by_gpu_model(self, gpu_model: str) -> List[CloudInstance]:
        """Get all instances with a specific GPU model."""
        return [i for i in self.instances if i.gpu_model.lower() == gpu_model.lower()]

    def get_training_instances(self) -> List[CloudInstance]:
        """Get instances optimized for training."""
        return [i for i in self.instances if i.training_optimized]

    def get_inference_instances(self) -> List[CloudInstance]:
        """Get instances optimized for inference."""
        return [i for i in self.instances if i.inference_optimized]

    def compare_providers_for_training(
        self,
        training_hours: float,
        use_spot: bool = False
    ) -> Dict[str, Any]:
        """Compare providers for training workload cost.

        Args:
            training_hours: Total training time in hours
            use_spot: Whether to use spot pricing

        Returns:
            Comparison data across providers

        Raises:
            ValueError: If training_hours is invalid
        """
        if training_hours <= 0:
            raise ValueError(f"Training hours must be positive: {training_hours}")

        providers = ['AWS', 'Azure', 'GCP']
        comparison = {}

        for provider in providers:
            provider_instances = self.get_instances_by_provider(provider)
            training_capable = [i for i in provider_instances if i.training_optimized]

            if not training_capable:
                continue

            # Find most cost-effective instance
            best_instance = None
            best_cost = float('inf')

            for instance in training_capable:
                try:
                    cost_calc = instance.calculate_training_cost(
                        training_hours=training_hours,
                        use_spot=use_spot
                    )
                    if cost_calc['total_cost_usd'] < best_cost:
                        best_cost = cost_calc['total_cost_usd']
                        best_instance = instance
                except ValueError:
                    # Skip instances that don't support requested pricing model
                    continue

            if best_instance:
                comparison[provider] = {
                    'instance_type': best_instance.instance_type,
                    'gpu_model': best_instance.gpu_model,
                    'gpu_count': best_instance.gpu_count,
                    'total_tflops_fp32': best_instance.tflops_fp32,
                    'total_cost_usd': best_cost,
                    'hourly_rate': best_instance.price_spot_hourly if use_spot else best_instance.price_ondemand_hourly,
                    'cost_per_tflop_hour': best_cost / training_hours / best_instance.tflops_fp32 if best_instance.tflops_fp32 > 0 else 0,
                }

        return comparison

    def compare_providers_for_inference(
        self,
        requests_per_second: float,
        avg_tokens_per_request: int,
        tokens_per_second_per_gpu: float,
        days: int = 30
    ) -> Dict[str, Any]:
        """Compare providers for inference workload cost.

        Args:
            requests_per_second: Expected RPS
            avg_tokens_per_request: Average tokens per request
            tokens_per_second_per_gpu: Throughput per GPU
            days: Number of days to run

        Returns:
            Comparison data across providers

        Raises:
            ValueError: If inputs are invalid
        """
        if requests_per_second < 0:
            raise ValueError(f"RPS cannot be negative: {requests_per_second}")
        if avg_tokens_per_request < 0:
            raise ValueError(f"Tokens per request cannot be negative: {avg_tokens_per_request}")
        if tokens_per_second_per_gpu <= 0:
            raise ValueError(f"Tokens per second per GPU must be positive: {tokens_per_second_per_gpu}")
        if days <= 0:
            raise ValueError(f"Days must be positive: {days}")

        providers = ['AWS', 'Azure', 'GCP']
        comparison = {}

        for provider in providers:
            provider_instances = self.get_instances_by_provider(provider)
            inference_capable = [i for i in provider_instances if i.inference_optimized or i.ml_optimized]

            if not inference_capable:
                continue

            # Find most cost-effective instance
            best_instance = None
            best_cost = float('inf')
            best_calc = None

            for instance in inference_capable:
                try:
                    cost_calc = instance.calculate_inference_cost(
                        requests_per_second=requests_per_second,
                        avg_tokens_per_request=avg_tokens_per_request,
                        tokens_per_second_per_gpu=tokens_per_second_per_gpu,
                        days=days
                    )
                    if cost_calc['compute_cost_usd'] < best_cost:
                        best_cost = cost_calc['compute_cost_usd']
                        best_instance = instance
                        best_calc = cost_calc
                except ValueError:
                    # Skip instances with invalid configurations
                    continue

            if best_instance and best_calc:
                comparison[provider] = {
                    'instance_type': best_instance.instance_type,
                    'gpu_model': best_instance.gpu_model,
                    'gpu_count': best_instance.gpu_count,
                    'total_cost_usd': best_calc['compute_cost_usd'],
                    'instances_needed': best_calc['instances_needed'],
                    'cost_per_1k_requests': best_calc['cost_per_1k_requests'],
                    'cost_per_1m_tokens': best_calc['cost_per_1m_tokens'],
                }

        return comparison

    def get_cost_efficiency_ranking(
        self,
        workload_type: str = 'training'
    ) -> List[Dict[str, Any]]:
        """Rank instances by cost efficiency.

        Args:
            workload_type: 'training' or 'inference'

        Returns:
            List of instances ranked by cost efficiency

        Raises:
            ValueError: If workload_type is invalid
        """
        valid_workload_types = ['training', 'inference']
        if workload_type not in valid_workload_types:
            raise ValueError(
                f"Invalid workload type: '{workload_type}'. "
                f"Must be one of: {valid_workload_types}"
            )

        if workload_type == 'training':
            candidates = self.get_training_instances()
        else:
            candidates = self.get_inference_instances()

        if not candidates:
            return []  # Return empty list if no instances match criteria

        ranking = []
        for instance in candidates:
            metrics = instance.compute_cost_metrics()
            if 'tflops_per_dollar' in metrics:
                ranking.append({
                    'provider': instance.provider,
                    'instance_type': instance.instance_type,
                    'gpu_model': instance.gpu_model,
                    'gpu_count': instance.gpu_count,
                    'tflops_per_dollar': metrics['tflops_per_dollar'],
                    'cost_per_tflop_hour': metrics.get('cost_per_tflop_hour', 0),
                    'price_ondemand_hourly': instance.price_ondemand_hourly,
                    'price_spot_hourly': instance.price_spot_hourly,
                })

        # Sort by TFLOPS per dollar (descending)
        ranking.sort(key=lambda x: x['tflops_per_dollar'], reverse=True)
        return ranking

    def get_spot_savings_analysis(self) -> List[Dict[str, Any]]:
        """Analyze potential savings from spot instances.

        Returns:
            List of instances with spot savings data
        """
        analysis = []
        for instance in self.instances:
            if instance.price_spot_hourly > 0 and instance.price_ondemand_hourly > 0:
                metrics = instance.compute_cost_metrics()
                savings_percent = metrics.get('spot_discount_percent', 0)
                annual_savings = (instance.price_ondemand_hourly - instance.price_spot_hourly) * 24 * 365

                analysis.append({
                    'provider': instance.provider,
                    'instance_type': instance.instance_type,
                    'gpu_model': instance.gpu_model,
                    'gpu_count': instance.gpu_count,
                    'ondemand_hourly': instance.price_ondemand_hourly,
                    'spot_hourly': instance.price_spot_hourly,
                    'savings_percent': savings_percent,
                    'annual_savings_usd': annual_savings,
                })

        # Sort by savings percentage
        analysis.sort(key=lambda x: x['savings_percent'], reverse=True)
        return analysis

    def estimate_llm_training_cost(
        self,
        parameters_billions: float,
        training_tokens_billions: float,
        tflops_per_token_per_param: float = 6.0,
        instance_type: Optional[str] = None,
        use_spot: bool = True
    ) -> Dict[str, Any]:
        """Estimate cost to train an LLM.

        Args:
            parameters_billions: Model size in billions of parameters
            training_tokens_billions: Training tokens in billions
            tflops_per_token_per_param: FLOPs multiplier (default 6 for standard training)
            instance_type: Specific instance to use (optional)
            use_spot: Whether to use spot pricing

        Returns:
            Cost estimate breakdown

        Raises:
            ValueError: If inputs are invalid or no suitable instances found
        """
        # Validate inputs
        if parameters_billions <= 0:
            raise ValueError(f"Parameters must be positive: {parameters_billions}B")
        if training_tokens_billions <= 0:
            raise ValueError(f"Training tokens must be positive: {training_tokens_billions}B")
        if tflops_per_token_per_param <= 0:
            raise ValueError(f"FLOPs multiplier must be positive: {tflops_per_token_per_param}")

        # Calculate total FLOPs needed
        # Formula: params * tokens * 6 (FLOPs per token per parameter for forward+backward pass)
        total_flops = parameters_billions * 1e9 * training_tokens_billions * 1e9 * tflops_per_token_per_param

        # Convert to TFLOPs (total compute needed)
        total_tflops = total_flops / 1e12

        # Find best instance
        if instance_type:
            instance = self.get_instance_by_type(instance_type)
            if not instance:
                raise ValueError(f"Instance type '{instance_type}' not found in dataset")
        else:
            # Use best training instance (A100 or H100)
            training_instances = self.get_training_instances()

            if not training_instances:
                raise ValueError("No training-optimized instances found in dataset")

            # Prefer H100 instances
            h100_instances = [i for i in training_instances if 'H100' in i.gpu_model]
            if h100_instances:
                instance = max(h100_instances, key=lambda x: x.tflops_fp16 if x.tflops_fp16 > 0 else 0)
            else:
                a100_instances = [i for i in training_instances if 'A100' in i.gpu_model]
                if a100_instances:
                    instance = max(a100_instances, key=lambda x: x.tflops_fp16 if x.tflops_fp16 > 0 else 0)
                else:
                    # Fallback to any instance with FP16 performance
                    instances_with_fp16 = [i for i in training_instances if i.tflops_fp16 > 0]
                    if not instances_with_fp16:
                        raise ValueError("No instances with FP16 TFLOPS data available")
                    instance = max(instances_with_fp16, key=lambda x: x.tflops_fp16)

        # Validate instance has FP16 performance data
        if instance.tflops_fp16 <= 0:
            raise ValueError(
                f"Instance {instance.instance_type} has no FP16 performance data. "
                f"TFLOPS FP16: {instance.tflops_fp16}"
            )

        # Calculate training time (assuming FP16 training with 50% utilization)
        # effective_tflops_per_second = TFLOPS rating * utilization
        effective_tflops_per_second = instance.tflops_fp16 * 0.5

        # Training time in seconds = total TFLOPs / TFLOPS per second
        training_seconds = total_tflops / effective_tflops_per_second

        # Convert to hours
        training_hours = training_seconds / 3600

        # Calculate cost
        cost_result = instance.calculate_training_cost(
            training_hours=training_hours,
            storage_gb=parameters_billions * 10,  # Rough estimate: 10GB per billion params
            storage_months=training_hours / 720,  # Convert hours to months
            use_spot=use_spot
        )

        return {
            'model_size_params': f"{parameters_billions}B",
            'training_tokens': f"{training_tokens_billions}B",
            'total_flops': total_flops,
            'total_tflops': total_tflops,
            'provider': instance.provider,
            'instance_type': instance.instance_type,
            'gpu_model': instance.gpu_model,
            'gpu_count': instance.gpu_count,
            'training_days': training_hours / 24,
            **cost_result
        }

    def get_gpu_price_evolution(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get price evolution for different GPU models.

        Returns:
            Dictionary mapping GPU models to price data over time
        """
        gpu_models = set(i.gpu_model for i in self.instances if i.gpu_model)
        evolution = {}

        for gpu_model in gpu_models:
            instances = self.get_instances_by_gpu_model(gpu_model)
            price_data = []

            for instance in instances:
                metrics = instance.compute_cost_metrics()
                price_data.append({
                    'year': instance.year,
                    'provider': instance.provider,
                    'instance_type': instance.instance_type,
                    'price_ondemand_hourly': instance.price_ondemand_hourly,
                    'cost_per_gpu_hour': metrics.get('cost_per_gpu_hour', 0),
                    'tflops_per_dollar': metrics.get('tflops_per_dollar', 0),
                })

            # Sort by year
            price_data.sort(key=lambda x: x['year'])
            evolution[gpu_model] = price_data

        return evolution

    def get_provider_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics per provider.

        Returns:
            Dictionary with statistics for each provider
        """
        providers = set(i.provider for i in self.instances)
        stats = {}

        for provider in providers:
            provider_instances = self.get_instances_by_provider(provider)

            if not provider_instances:
                continue

            # Calculate averages
            avg_price = sum(i.price_ondemand_hourly for i in provider_instances) / len(provider_instances)
            avg_spot_discount = sum(
                i.compute_cost_metrics().get('spot_discount_percent', 0)
                for i in provider_instances
                if i.price_spot_hourly > 0
            ) / max(1, sum(1 for i in provider_instances if i.price_spot_hourly > 0))

            total_gpus = sum(i.gpu_count for i in provider_instances)
            gpu_models = set(i.gpu_model for i in provider_instances if i.gpu_model)

            stats[provider] = {
                'instance_count': len(provider_instances),
                'avg_hourly_cost': avg_price,
                'avg_spot_discount_percent': avg_spot_discount,
                'total_gpus': total_gpus,
                'unique_gpu_models': len(gpu_models),
                'gpu_models': sorted(list(gpu_models)),
                'training_instances': sum(1 for i in provider_instances if i.training_optimized),
                'inference_instances': sum(1 for i in provider_instances if i.inference_optimized),
                'price_range': {
                    'min': min(i.price_ondemand_hourly for i in provider_instances),
                    'max': max(i.price_ondemand_hourly for i in provider_instances),
                }
            }

        return stats

    def compare_instance_specs(
        self,
        instance_types: List[str]
    ) -> List[Dict[str, Any]]:
        """Compare specifications of multiple instances.

        Args:
            instance_types: List of instance type names

        Returns:
            List of instance specs for comparison
        """
        comparison = []

        for instance_type in instance_types:
            instance = self.get_instance_by_type(instance_type)
            if instance:
                metrics = instance.compute_cost_metrics()
                comparison.append({
                    'provider': instance.provider,
                    'instance_type': instance.instance_type,
                    'gpu_model': instance.gpu_model,
                    'gpu_count': instance.gpu_count,
                    'gpu_memory_gb': instance.gpu_memory_gb,
                    'total_gpu_memory_gb': instance.gpu_memory_gb * instance.gpu_count,
                    'vcpus': instance.vcpus,
                    'ram_gb': instance.ram_gb,
                    'tflops_fp32': instance.tflops_fp32,
                    'tflops_fp16': instance.tflops_fp16,
                    'price_ondemand_hourly': instance.price_ondemand_hourly,
                    'price_spot_hourly': instance.price_spot_hourly,
                    'tflops_per_dollar': metrics.get('tflops_per_dollar', 0),
                    'cost_per_gpu_hour': metrics.get('cost_per_gpu_hour', 0),
                })

        return comparison

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Get summary statistics for all cloud instances."""
        if not self.instances:
            return {}

        providers = set(i.provider for i in self.instances)
        gpu_models = set(i.gpu_model for i in self.instances if i.gpu_model)

        total_training = sum(1 for i in self.instances if i.training_optimized)
        total_inference = sum(1 for i in self.instances if i.inference_optimized)

        return {
            'total_instances': len(self.instances),
            'providers': list(providers),
            'provider_count': len(providers),
            'gpu_models': sorted(list(gpu_models)),
            'unique_gpu_models': len(gpu_models),
            'training_instances': total_training,
            'inference_instances': total_inference,
            'price_range': {
                'min': min(i.price_ondemand_hourly for i in self.instances),
                'max': max(i.price_ondemand_hourly for i in self.instances),
                'avg': sum(i.price_ondemand_hourly for i in self.instances) / len(self.instances)
            },
            'year_range': f"{min(i.year for i in self.instances)}-{max(i.year for i in self.instances)}"
        }

    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert all instances to dictionaries."""
        return [instance.to_dict() for instance in self.instances]
