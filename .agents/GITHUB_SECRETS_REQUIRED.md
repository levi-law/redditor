# GitHub Secrets Required for CI/CD

Please configure the following secrets in your GitHub repository settings:
**Settings → Secrets and variables → Actions → New repository secret**

Repository URL: https://github.com/levi-law/redditor/settings/secrets/actions

---

## 🔑 Required Secrets

### Reddit API Credentials
| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `REDDIT_CLIENT_ID` | Reddit OAuth application Client ID | [Reddit Apps](https://www.reddit.com/prefs/apps) - Create a "script" type app |
| `REDDIT_CLIENT_SECRET` | Reddit OAuth application Client Secret | Same as above, shown after creating the app |
| `REDDIT_USERNAME` | Your Reddit username | Your Reddit account username |
| `REDDIT_PASSWORD` | Your Reddit password | Your Reddit account password |

### AI Provider API Keys
| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | [OpenAI API Keys](https://platform.openai.com/api-keys) |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | [Anthropic Console](https://console.anthropic.com/) |

---

## 📦 Optional Secrets (for CD/Release)

### PyPI Publishing
| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `PYPI_API_TOKEN` | PyPI API token for package publishing | [PyPI Account Settings](https://pypi.org/manage/account/#api-tokens) |

### Docker Hub
| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `DOCKERHUB_USERNAME` | Docker Hub username | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token | [Docker Hub Security](https://hub.docker.com/settings/security) |

### Code Coverage
| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `CODECOV_TOKEN` | Codecov upload token | [Codecov](https://app.codecov.io/) - Add repository |

---

## ✅ Quick Setup Checklist

- [ ] `REDDIT_CLIENT_ID` - **Required for tests**
- [ ] `REDDIT_CLIENT_SECRET` - **Required for tests**
- [ ] `REDDIT_USERNAME` - **Required for tests** 
- [ ] `REDDIT_PASSWORD` - **Required for tests**
- [ ] `OPENAI_API_KEY` - **Required for AI features**
- [ ] `ANTHROPIC_API_KEY` - **Required for AI features**
- [ ] `PYPI_API_TOKEN` - Optional (for PyPI releases)
- [ ] `DOCKERHUB_USERNAME` - Optional (for Docker images)
- [ ] `DOCKERHUB_TOKEN` - Optional (for Docker images)
- [ ] `CODECOV_TOKEN` - Optional (for coverage reports)

---

## 🚀 After Setting Secrets

1. Push this commit to trigger CI:
   ```bash
   git add .
   git commit -m "Add CI/CD workflows"
   git push origin main
   ```

2. Check workflow status at:
   https://github.com/levi-law/redditor/actions
