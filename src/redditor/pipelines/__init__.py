"""Pipeline framework module."""

from redditor.pipelines.base import Pipeline
from redditor.pipelines.registry import PipelineRegistry

__all__ = ["Pipeline", "PipelineRegistry"]
