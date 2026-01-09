"""CLI for Redditor - AI-Powered Reddit Agent System.

Provides commands for managing and running Reddit agent pipelines.
"""

import click
from typing import Optional

from redditor import __version__
from redditor.config import get_settings


@click.group()
@click.version_option(version=__version__, prog_name="redditor")
@click.option("--debug/--no-debug", default=False, help="Enable debug mode")
@click.pass_context
def main(ctx: click.Context, debug: bool) -> None:
    """Redditor - AI-Powered Reddit Agent System.
    
    Manage and run AI agent pipelines for Reddit automation tasks
    including content analysis, engagement, and monitoring.
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["settings"] = get_settings()


@main.group()
@click.pass_context
def pipeline(ctx: click.Context) -> None:
    """Pipeline management commands.
    
    List, run, and manage Reddit agent pipelines.
    """
    pass


@pipeline.command("list")
@click.pass_context
def pipeline_list(ctx: click.Context) -> None:
    """List all available pipelines."""
    from redditor.pipelines.registry import PipelineRegistry
    
    registry = PipelineRegistry()
    pipelines = registry.all()
    
    if not pipelines:
        click.echo("No pipelines registered yet.")
        return
    
    click.echo("Available pipelines:")
    for name in pipelines:
        click.echo(f"  • {name}")


@pipeline.command("run")
@click.argument("name")
@click.option("--subreddit", "-s", help="Target subreddit")
@click.option("--limit", "-l", default=10, help="Number of items to process")
@click.pass_context
def pipeline_run(
    ctx: click.Context,
    name: str,
    subreddit: Optional[str],
    limit: int,
) -> None:
    """Run a specific pipeline.
    
    NAME is the name of the pipeline to execute.
    """
    from redditor.pipelines.registry import PipelineRegistry
    
    registry = PipelineRegistry()
    pipeline_cls = registry.get(name)
    
    if pipeline_cls is None:
        click.echo(f"Pipeline '{name}' not found.", err=True)
        ctx.exit(1)
    
    config = {}
    if subreddit:
        config["subreddit"] = subreddit
    config["limit"] = limit
    
    click.echo(f"Running pipeline: {name}")
    
    try:
        pipeline = pipeline_cls(config=config)
        pipeline.setup()
        result = pipeline.execute()
        pipeline.cleanup()
        
        click.echo(f"Pipeline completed: {result}")
    except Exception as e:
        click.echo(f"Pipeline failed: {e}", err=True)
        if ctx.obj.get("debug"):
            raise
        ctx.exit(1)


@main.group()
@click.pass_context
def config(ctx: click.Context) -> None:
    """Configuration management commands."""
    pass


@config.command("show")
@click.option("--secrets/--no-secrets", default=False, help="Show secret values")
@click.pass_context
def config_show(ctx: click.Context, secrets: bool) -> None:
    """Display current configuration."""
    settings = ctx.obj["settings"]
    
    click.echo("Redditor Configuration")
    click.echo("=" * 40)
    click.echo(f"Debug Mode: {settings.debug}")
    click.echo(f"Log Level: {settings.log_level}")
    click.echo()
    
    click.echo("Reddit API:")
    click.echo(f"  Client ID: {'*' * 8 if settings.reddit.client_id else '(not set)'}")
    click.echo(f"  User Agent: {settings.reddit.user_agent}")
    click.echo(f"  Username: {settings.reddit.username or '(not set)'}")
    click.echo()
    
    click.echo("AI Configuration:")
    click.echo(f"  OpenAI: {'configured' if settings.ai.openai_api_key else 'not configured'}")
    click.echo(f"  Anthropic: {'configured' if settings.ai.anthropic_api_key else 'not configured'}")
    click.echo()
    
    click.echo("Database:")
    click.echo(f"  URL: {settings.database.url}")


@config.command("check")
@click.pass_context
def config_check(ctx: click.Context) -> None:
    """Verify configuration is valid."""
    settings = ctx.obj["settings"]
    
    issues = []
    
    if not settings.is_reddit_configured():
        issues.append("Reddit API credentials not configured")
    
    if not settings.is_ai_configured():
        issues.append("No AI API keys configured")
    
    if issues:
        click.echo("Configuration issues found:", err=True)
        for issue in issues:
            click.echo(f"  ✗ {issue}", err=True)
        ctx.exit(1)
    else:
        click.echo("✓ Configuration is valid")


if __name__ == "__main__":
    main()
