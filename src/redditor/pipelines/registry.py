"""Pipeline registry for discovering and managing pipelines.

Provides a central registry for all available pipelines with
registration, lookup, and listing capabilities.
"""

from typing import Optional, Type

from redditor.pipelines.base import Pipeline


class PipelineRegistry:
    """Central registry for pipeline classes.
    
    Allows registration and lookup of pipelines by name.
    
    Example:
        ```python
        registry = PipelineRegistry()
        registry.register(MyPipeline)
        
        pipeline_cls = registry.get("my_pipeline")
        pipeline = pipeline_cls(config={})
        ```
    """
    
    # Class-level registry shared across instances
    _pipelines: dict[str, Type[Pipeline]] = {}
    
    def __init__(self):
        """Initialize the registry."""
        # Use instance-level dict if we want isolated registries
        # For now, share class-level registry
        pass
    
    def register(self, pipeline_cls: Type[Pipeline]) -> None:
        """Register a pipeline class.
        
        Args:
            pipeline_cls: Pipeline class to register
            
        Raises:
            TypeError: If pipeline_cls is not a Pipeline subclass
            ValueError: If a pipeline with the same name exists
        """
        if not isinstance(pipeline_cls, type) or not issubclass(pipeline_cls, Pipeline):
            raise TypeError(f"Expected Pipeline subclass, got {type(pipeline_cls)}")
        
        # Create temporary instance to get name
        # This works because we're not calling execute()
        try:
            # For abstract classes, we need to check differently
            if hasattr(pipeline_cls, "name") and isinstance(
                getattr(pipeline_cls, "name", None), property
            ):
                # Create a minimal test instance
                class TempPipeline(pipeline_cls):
                    @property
                    def name(self):
                        return super().name
                    
                    def execute(self):
                        return {}
                
                temp = TempPipeline()
                name = temp.name
            else:
                # Try direct instantiation
                temp = pipeline_cls()
                name = temp.name
        except TypeError:
            # Abstract class - use class name as fallback
            name = pipeline_cls.__name__.lower().replace("pipeline", "")
        
        self._pipelines[name] = pipeline_cls
    
    def get(self, name: str) -> Optional[Type[Pipeline]]:
        """Get a pipeline class by name.
        
        Args:
            name: Pipeline name
            
        Returns:
            Pipeline class if found, None otherwise
        """
        return self._pipelines.get(name)
    
    def all(self) -> dict[str, Type[Pipeline]]:
        """Get all registered pipelines.
        
        Returns:
            Dictionary mapping names to pipeline classes
        """
        return dict(self._pipelines)
    
    def __contains__(self, name: str) -> bool:
        """Check if a pipeline name is registered."""
        return name in self._pipelines
    
    def clear(self) -> None:
        """Clear all registered pipelines."""
        self._pipelines.clear()


# Global registry instance
_global_registry = PipelineRegistry()


def register_pipeline(cls: Type[Pipeline]) -> Type[Pipeline]:
    """Decorator to register a pipeline with the global registry.
    
    Example:
        ```python
        @register_pipeline
        class MyPipeline(Pipeline):
            ...
        ```
    """
    _global_registry.register(cls)
    return cls


def get_global_registry() -> PipelineRegistry:
    """Get the global pipeline registry."""
    return _global_registry
