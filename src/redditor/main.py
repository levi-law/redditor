"""FastAPI application entry point for Redditor."""

from fastapi import FastAPI

from redditor import __version__


app = FastAPI(
    title="Redditor API",
    description="AI-Powered Reddit Agent System",
    version=__version__,
)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Redditor API",
        "version": __version__,
        "status": "operational",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()
