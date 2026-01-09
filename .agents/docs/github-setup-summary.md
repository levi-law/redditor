# Redditor Project - GitHub Setup & CI/CD Summary

## Repository Created
**URL**: https://github.com/levi-law/redditor

> ⚠️ **Note**: Created under `levi-law` account because `roeiba` token was invalid.  
> Run `gh auth login -h github.com` to fix if you want to use a different account.

---

## CI/CD Workflows

### CI Workflow (`.github/workflows/ci.yml`)
**Triggers**: Push/PR to `main` or `develop`

| Job | Description |
|-----|-------------|
| **Lint** | Ruff, Black, MyPy checks |
| **Test** | pytest on Python 3.11 & 3.12 with coverage |
| **Security** | Safety (deps) + Bandit (code) scans |

### CD Workflow (`.github/workflows/cd.yml`)
**Triggers**: Release/Tags `v*.*.*`

| Job | Description |
|-----|-------------|
| **Build** | Creates Python package |
| **Publish PyPI** | Uploads to PyPI on release |
| **Docker** | Builds & pushes Docker image |

---

## Secrets Configuration

### Files Created
- `.agents/secrets.env` - Template for credentials
- `.agents/upload_secrets.sh` - Script to upload to GitHub

### Required Secrets

| Secret | Required For |
|--------|-------------|
| `REDDIT_CLIENT_ID` | Tests (PRAW) |
| `REDDIT_CLIENT_SECRET` | Tests (PRAW) |
| `REDDIT_USERNAME` | Tests |
| `REDDIT_PASSWORD` | Tests |
| `OPENAI_API_KEY` | AI features |
| `ANTHROPIC_API_KEY` | AI features |
| `PYPI_API_TOKEN` | PyPI releases |
| `DOCKERHUB_USERNAME` | Docker images |
| `DOCKERHUB_TOKEN` | Docker images |
| `CODECOV_TOKEN` | Coverage reports |

### To Configure
1. Edit `.agents/secrets.env` with your values
2. Run `.agents/upload_secrets.sh`

---

## Architectural Decision

**Outcome**: Migrate from PRAW (Python) to **Devvit (TypeScript)**

### Why Devvit?
1. ✅ No API approval wait
2. ✅ Real-time event triggers
3. ✅ Built-in Redis storage
4. ✅ Zero infrastructure management
5. ✅ Reddit handles hosting

### Documentation Created
- `.agents/docs/reddit-platforms-comparison.md`
- `.agents/docs/devvit-quickstart.md`
- `.agents/docs/devvit-api-reference.md`
- `.agents/docs/architecture-decision.md`

---

## Next Steps

1. [ ] Initialize Devvit project structure
2. [ ] Set up TypeScript configuration
3. [ ] Port pipeline framework to TypeScript
4. [ ] Update CI/CD for Devvit (npm-based)
5. [ ] Request domain approval for OpenAI/Anthropic
