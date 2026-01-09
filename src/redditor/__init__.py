"""Redditor - AI-Powered Reddit Agent System.

A collection of AI agent pipelines for automating Reddit tasks.
"""

__version__ = "0.1.0"
__author__ = "AgenticCompany"

from redditor.config import Settings
from redditor.reddit.client import RedditClient
from redditor.pipelines.base import Pipeline
from redditor.pipelines.registry import PipelineRegistry

__all__ = [
    "__version__",
    "Settings",
    "RedditClient",
    "Pipeline",
    "PipelineRegistry",
]
