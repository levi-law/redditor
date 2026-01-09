# Reddit Developer Platforms Comparison

> **Last Updated**: January 2026  
> **Purpose**: Guide for choosing between Reddit's two developer platforms

## Overview

Reddit offers two distinct developer platforms with different use cases:

| Platform | URL | Purpose |
|----------|-----|---------|
| **Devvit** | `developers.reddit.com` | Apps running ON Reddit's infrastructure |
| **Data API** | `reddit.com/prefs/apps` | External bots/scripts (PRAW) |

---

## Devvit (Recommended for New Projects)

### What Is It?
Devvit is Reddit's modern developer platform for building interactive experiences that run directly on Reddit's servers. Apps are written in TypeScript and hosted by Reddit.

### Key Features
- **Real-time Triggers**: React instantly to events (`onPostSubmit`, `onCommentCreate`, `onModAction`)
- **Scheduler**: Cron-like background jobs for automation
- **Redis Storage**: Built-in database per installation
- **External APIs**: Call OpenAI, Anthropic, etc. via `fetch` (requires domain approval)
- **No Infrastructure**: Reddit handles hosting, scaling, uptime

### API Capabilities
```typescript
// Comments
context.reddit.submitComment({ id: postId, text: "Hello!" })
context.reddit.getComments({ postId })

// Posts
context.reddit.getHotPosts({ subredditName })
context.reddit.getNewPosts({ subredditName })
context.reddit.submitPost({ subredditName, title, text })

// DMs
context.reddit.sendPrivateMessage({ to: username, subject, text })
context.reddit.sendPrivateMessageAsSubreddit({ ... })

// Users
context.reddit.getCurrentUser()
context.reddit.getUserById(userId)
```

### Limitations
- **Subreddit-scoped**: Apps must be installed in each subreddit individually
- **Rate Limits**: 60 scheduled actions/minute, 10 recurring jobs per install
- **Domain Approval**: External API calls require Reddit review
- **TypeScript Only**: No Python support

### When to Use Devvit
✅ Building a subreddit-specific bot or mod tool  
✅ Need real-time event triggers  
✅ Want zero infrastructure management  
✅ Building interactive Reddit experiences  

---

## Data API (Classic PRAW)

### What Is It?
The original Reddit API for external applications. Uses OAuth2 with Client ID/Secret. Accessed via PRAW (Python) or similar libraries.

### Key Features
- **Global Access**: Read/write to any public subreddit
- **Self-Hosted**: Run anywhere (your server, CI/CD, local)
- **Python Ecosystem**: PRAW, asyncpraw, and rich Python tooling
- **Flexible Authentication**: Script, web, or installed app types

### Current Status (2026)
⚠️ **Access is now restricted**. You must:
1. Register as a developer at `reddit.com/wiki/api`
2. Submit an API Access Request form
3. Wait for approval (can take days)

### When to Use Data API
✅ Need to scan/interact across many subreddits  
✅ Building a global monitoring/analytics tool  
✅ Require Python and existing PRAW codebase  
✅ Self-hosting is preferred  

---

## Comparison Matrix

| Feature | Devvit | Data API (PRAW) |
|---------|--------|-----------------|
| **Language** | TypeScript | Python |
| **Hosting** | Reddit servers | Self-hosted |
| **Auth Setup** | `devvit login` CLI | OAuth Client ID/Secret |
| **Real-time Triggers** | ✅ Native | ❌ Polling required |
| **Background Jobs** | ✅ Scheduler | ❌ External cron needed |
| **Data Storage** | ✅ Redis built-in | ❌ Bring your own DB |
| **Multi-subreddit** | ⚠️ Per-installation | ✅ Global access |
| **API Approval** | ✅ Immediate | ⚠️ Request required |
| **External APIs** | ⚠️ Domain approval | ✅ Unrestricted |

---

## Decision: Devvit for Redditor Project

Given the current landscape, **Devvit is the recommended platform** for the Redditor AI agent:

1. **No API approval wait** - Start building immediately
2. **Real-time triggers** - Better than polling for responsiveness
3. **Zero infrastructure** - Reddit handles hosting
4. **Built-in storage** - Redis for conversation history
5. **Modern stack** - TypeScript, event-driven architecture

The tradeoff (per-subreddit installation) is acceptable for most AI agent use cases where you want deep integration with specific communities rather than broad, shallow access across all of Reddit.
