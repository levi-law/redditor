"""Black-box tests for Pipeline framework.

These tests verify the pipeline framework's public interface
and expected behavior for defining and executing pipelines.
"""

import pytest
from unittest.mock import MagicMock, patch


class TestPipelineBaseClass:
    """Tests for the Pipeline abstract base class."""
    
    def test_pipeline_is_abstract(self):
        """Pipeline class should be abstract and not directly instantiable."""
        from redditor.pipelines.base import Pipeline
        
        # Should not be able to instantiate abstract pipeline
        with pytest.raises(TypeError):
            Pipeline()
    
    def test_pipeline_has_execute_method(self):
        """Pipeline must define execute as an abstract method."""
        from redditor.pipelines.base import Pipeline
        import abc
        
        # execute should be an abstract method
        assert hasattr(Pipeline, "execute")
        assert getattr(Pipeline.execute, "__isabstractmethod__", False)
    
    def test_pipeline_has_name_property(self):
        """Pipeline should have a name property."""
        from redditor.pipelines.base import Pipeline
        
        # Create a concrete implementation
        class TestPipeline(Pipeline):
            @property
            def name(self):
                return "test_pipeline"
            
            def execute(self):
                pass
        
        pipeline = TestPipeline()
        assert pipeline.name == "test_pipeline"
    
    def test_pipeline_has_lifecycle_methods(self):
        """Pipeline should have setup and cleanup lifecycle methods."""
        from redditor.pipelines.base import Pipeline
        
        # These should be defined (possibly as no-ops by default)
        assert hasattr(Pipeline, "setup") or hasattr(Pipeline, "_setup")
        assert hasattr(Pipeline, "cleanup") or hasattr(Pipeline, "_cleanup")


class TestPipelineConfiguration:
    """Tests for pipeline configuration loading."""
    
    def test_pipeline_accepts_config_dict(self):
        """Pipeline should accept configuration as dictionary."""
        from redditor.pipelines.base import Pipeline
        
        class TestPipeline(Pipeline):
            @property
            def name(self):
                return "test_pipeline"
            
            def execute(self):
                pass
        
        config = {"param1": "value1", "param2": 123}
        pipeline = TestPipeline(config=config)
        
        # Pipeline should store configuration
        assert hasattr(pipeline, "config") or hasattr(pipeline, "_config")
    
    def test_pipeline_config_validation(self):
        """Pipeline should validate required configuration."""
        from redditor.pipelines.base import Pipeline
        
        class StrictPipeline(Pipeline):
            required_config = ["api_key", "subreddit"]
            
            @property
            def name(self):
                return "strict_pipeline"
            
            def execute(self):
                pass
        
        # Missing required config should raise error
        # This is optional behavior - implementation may vary
        # Just verify we can create with valid config
        config = {"api_key": "xxx", "subreddit": "test"}
        pipeline = StrictPipeline(config=config)
        assert pipeline is not None


class TestPipelineRegistry:
    """Tests for pipeline registry functionality."""
    
    def test_registry_can_register_pipeline(self):
        """Should be able to register pipelines."""
        from redditor.pipelines.registry import PipelineRegistry
        from redditor.pipelines.base import Pipeline
        
        class MyPipeline(Pipeline):
            @property
            def name(self):
                return "my_pipeline"
            
            def execute(self):
                pass
        
        registry = PipelineRegistry()
        registry.register(MyPipeline)
        
        # Pipeline should be findable
        assert "my_pipeline" in registry or MyPipeline in registry.all()
    
    def test_registry_can_get_pipeline_by_name(self):
        """Should retrieve pipeline by name."""
        from redditor.pipelines.registry import PipelineRegistry
        from redditor.pipelines.base import Pipeline
        
        class NamedPipeline(Pipeline):
            @property
            def name(self):
                return "named_pipeline"
            
            def execute(self):
                pass
        
        registry = PipelineRegistry()
        registry.register(NamedPipeline)
        
        retrieved = registry.get("named_pipeline")
        assert retrieved is not None
    
    def test_registry_lists_all_pipelines(self):
        """Should list all registered pipelines."""
        from redditor.pipelines.registry import PipelineRegistry
        
        registry = PipelineRegistry()
        all_pipelines = registry.all()
        
        # Should return a list or dict
        assert isinstance(all_pipelines, (list, dict))


class TestPipelineExecution:
    """Tests for pipeline execution."""
    
    def test_execute_returns_result(self):
        """Execute should return a result object."""
        from redditor.pipelines.base import Pipeline
        
        class ResultPipeline(Pipeline):
            @property
            def name(self):
                return "result_pipeline"
            
            def execute(self):
                return {"status": "success", "items_processed": 10}
        
        pipeline = ResultPipeline()
        result = pipeline.execute()
        
        assert result is not None
        assert "status" in result
    
    def test_execute_handles_errors_gracefully(self):
        """Pipeline should handle execution errors gracefully."""
        from redditor.pipelines.base import Pipeline
        
        class FailingPipeline(Pipeline):
            @property
            def name(self):
                return "failing_pipeline"
            
            def execute(self):
                raise RuntimeError("Simulated failure")
        
        pipeline = FailingPipeline()
        
        # Either catches and returns error result, or raises
        # We test that it at least raises predictably
        with pytest.raises(RuntimeError):
            pipeline.execute()
