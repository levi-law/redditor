"""Base Pipeline abstract class for Redditor agents.

Provides the foundation for all AI agent pipelines with a standard
lifecycle (setup, execute, cleanup) and configuration management.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class Pipeline(ABC):
    """Abstract base class for all Redditor pipelines.
    
    Defines the standard interface for AI agent pipelines with
    lifecycle methods and configuration handling.
    
    Attributes:
        config: Pipeline configuration dictionary
        logger: Logger instance for this pipeline
    
    Example:
        ```python
        class MyPipeline(Pipeline):
            @property
            def name(self):
                return "my_pipeline"
            
            def execute(self):
                # Do work
                return {"status": "success"}
        ```
    """
    
    # Optional: subclasses can define required config keys
    required_config: list[str] = []
    
    def __init__(self, config: Optional[dict[str, Any]] = None):
        """Initialize the pipeline with configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self._config = config or {}
        self._logger = logging.getLogger(f"{__name__}.{self.name}")
        
        # Validate required configuration
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate that required configuration keys are present."""
        missing = [key for key in self.required_config if key not in self._config]
        if missing:
            raise ValueError(f"Missing required config keys: {missing}")
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of this pipeline.
        
        Must be implemented by subclasses.
        
        Returns:
            Pipeline name string
        """
        pass
    
    @property
    def config(self) -> dict[str, Any]:
        """Get the pipeline configuration."""
        return self._config
    
    @property
    def logger(self) -> logging.Logger:
        """Get the pipeline's logger."""
        return self._logger
    
    def setup(self) -> None:
        """Prepare the pipeline for execution.
        
        Called before execute(). Override in subclasses for
        initialization logic like connecting to APIs or databases.
        
        Default implementation does nothing.
        """
        self._logger.debug(f"Setting up pipeline: {self.name}")
    
    def _setup(self) -> None:
        """Internal setup alias."""
        self.setup()
    
    @abstractmethod
    def execute(self) -> dict[str, Any]:
        """Execute the pipeline's main logic.
        
        Must be implemented by subclasses.
        
        Returns:
            Result dictionary with at minimum a 'status' key
        """
        pass
    
    def cleanup(self) -> None:
        """Clean up resources after execution.
        
        Called after execute() completes (success or failure).
        Override in subclasses for cleanup logic.
        
        Default implementation does nothing.
        """
        self._logger.debug(f"Cleaning up pipeline: {self.name}")
    
    def _cleanup(self) -> None:
        """Internal cleanup alias."""
        self.cleanup()
    
    def run(self) -> dict[str, Any]:
        """Run the complete pipeline lifecycle.
        
        Calls setup(), execute(), and cleanup() in order,
        ensuring cleanup runs even if execute() fails.
        
        Returns:
            Result from execute()
            
        Raises:
            Exception: If execute() raises an exception after cleanup
        """
        self.setup()
        try:
            result = self.execute()
            return result
        finally:
            self.cleanup()
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}')>"
