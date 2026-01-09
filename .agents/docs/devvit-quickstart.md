# Devvit Quickstart Guide

> **Official Docs**: https://developers.reddit.com/docs/quickstart/

## Prerequisites

- Node.js 22.2.0+
- npm
- Reddit account

## Setup Steps

### 1. Install Devvit CLI
```bash
npm install -g @reddit/devvit-cli
```

### 2. Authenticate
```bash
devvit login
```
This opens a browser for Reddit OAuth. Token is saved to `~/.devvit/token`.

### 3. Create New App

**Option A: Web Wizard**
1. Go to https://developers.reddit.com/new
2. Select template (Game, Mod Tool, or Custom)
3. Follow the wizard

**Option B: CLI**
```bash
devvit new my-reddit-app
cd my-reddit-app
npm install
```

### 4. Project Structure
```
my-reddit-app/
├── src/
│   └── main.tsx       # Main app entry point
├── devvit.yaml        # App configuration
├── package.json
└── tsconfig.json
```

### 5. Run Locally
```bash
npm run dev
```
This connects to a test subreddit for live development.

### 6. Deploy to Reddit
```bash
devvit upload
```

---

## Core Concepts

### Triggers (Event Handlers)
```typescript
import { Devvit } from '@devvit/public-api';

Devvit.addTrigger({
  event: 'PostSubmit',
  onEvent: async (event, context) => {
    const post = await context.reddit.getPostById(event.postId);
    await context.reddit.submitComment({
      id: post.id,
      text: `Thanks for posting, ${post.authorName}!`
    });
  }
});
```

**Available Triggers:**
- `PostSubmit` / `PostCreate` / `PostUpdate` / `PostDelete`
- `CommentCreate` / `CommentUpdate` / `CommentDelete`
- `ModAction` / `ModMail`
- `AppInstall` / `AppUpgrade`

### Scheduler (Background Jobs)
```typescript
Devvit.addSchedulerJob({
  name: 'daily-summary',
  onRun: async (event, context) => {
    // Runs on schedule
    const posts = await context.reddit.getHotPosts({ limit: 10 });
    // Process posts...
  }
});

// Schedule it (e.g., in an install trigger)
await context.scheduler.runJob({
  name: 'daily-summary',
  cron: '0 9 * * *'  // Daily at 9 AM
});
```

### Redis Storage
```typescript
// Store data
await context.redis.set('user:123:preferences', JSON.stringify(prefs));

// Retrieve data
const prefs = JSON.parse(await context.redis.get('user:123:preferences'));

// Hash operations
await context.redis.hSet('stats', { views: '100', likes: '50' });
const stats = await context.redis.hGetAll('stats');
```

### External API Calls
```typescript
// Must declare domain in devvit.yaml first
const response = await fetch('https://api.openai.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${await context.settings.get('openai_key')}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ model: 'gpt-4', messages: [...] })
});
```

**devvit.yaml:**
```yaml
name: my-reddit-app
version: 0.0.1
dependencies:
  strict: false
  domains:
    - api.openai.com
    - api.anthropic.com
```

---

## App Settings (Secrets)
```typescript
Devvit.addSettings([
  {
    name: 'openai_key',
    type: 'string',
    label: 'OpenAI API Key',
    isSecret: true,
    scope: 'installation'
  }
]);

// Access in code
const apiKey = await context.settings.get('openai_key');
```

Moderators set these values when installing your app.

---

## Useful Commands

| Command | Description |
|---------|-------------|
| `devvit login` | Authenticate with Reddit |
| `devvit new <name>` | Create new project |
| `devvit upload` | Deploy to Reddit |
| `devvit playtest <subreddit>` | Test in a real subreddit |
| `devvit logs` | View app logs |
| `devvit list apps` | List your apps |

---

## Rate Limits

| Resource | Limit |
|----------|-------|
| Scheduler jobs | 10 recurring per installation |
| Scheduler delivery | 60 actions/minute |
| Redis storage | Generous (check docs) |
| API calls | Standard Reddit limits |

---

## Resources

- **Docs**: https://developers.reddit.com/docs/
- **API Reference**: https://developers.reddit.com/docs/api/
- **Community**: r/Devvit
- **Examples**: https://github.com/reddit/devvit-examples
