# Architecture Decision Record: Reddit Platform Choice

**Date**: January 2026  
**Status**: Accepted  
**Decision**: Migrate Redditor from PRAW (Python) to Devvit (TypeScript)

---

## Context

The Redditor project was initially designed to use PRAW (Python Reddit API Wrapper) for Reddit automation. However, Reddit has significantly changed their API access policies:

1. **Self-service app creation is restricted** - The `reddit.com/prefs/apps` endpoint now requires pre-registration
2. **API Access Request required** - New developers must submit a form and wait for approval
3. **Devvit is the promoted platform** - Reddit is actively pushing developers toward Devvit

---

## Options Considered

### Option 1: Continue with PRAW
**Pros:**
- Existing Python codebase
- Global access to any subreddit
- Self-hosted, full control

**Cons:**
- Requires API access approval (unknown wait time)
- Need to manage hosting infrastructure
- Polling-based (no real-time events)
- No built-in storage

### Option 2: Switch to Devvit
**Pros:**
- No API approval wait - immediate access
- Real-time event triggers
- Built-in Redis storage
- Zero infrastructure management
- Reddit handles scaling and uptime
- Modern TypeScript codebase

**Cons:**
- Must rewrite in TypeScript
- Per-subreddit installation required
- External API domains require Reddit approval
- New platform, still evolving

### Option 3: Hybrid Approach
Build both: Devvit for per-subreddit features, PRAW for global scanning.

**Pros:**
- Best of both worlds

**Cons:**
- Double the maintenance
- Two codebases to manage
- Complexity overhead

---

## Decision

**We will adopt Devvit as the primary platform for Redditor.**

### Rationale

1. **Immediate Start**: No waiting for API approval
2. **Better Architecture**: Event-driven > polling for responsiveness
3. **Reduced Ops**: Reddit handles hosting, scaling, logging
4. **Storage Included**: Redis for conversation history, user preferences
5. **Future-Proof**: Devvit is Reddit's strategic direction

### Accepted Tradeoffs

- **Per-subreddit scope**: Acceptable for AI agents that deeply integrate with specific communities
- **TypeScript rewrite**: Actually beneficial for modern, type-safe development
- **Domain approval for AI APIs**: OpenAI/Anthropic domains are commonly approved

---

## Implementation Plan

### Phase 1: Foundation (Sprint v0.2)
- [ ] Initialize Devvit project
- [ ] Set up TypeScript configuration
- [ ] Create basic app structure
- [ ] Implement `devvit login` CI/CD

### Phase 2: Core Features (Sprint v0.3)
- [ ] Implement event triggers (PostSubmit, CommentCreate)
- [ ] Add Redis storage for conversation history
- [ ] Integrate OpenAI/Anthropic for AI responses
- [ ] Build settings UI for API keys

### Phase 3: AI Agent Logic (Sprint v0.4)
- [ ] Port pipeline framework to TypeScript
- [ ] Implement content analysis pipelines
- [ ] Add scheduling for periodic tasks
- [ ] Build moderation assistance features

### Phase 4: Polish (Sprint v0.5)
- [ ] Comprehensive testing
- [ ] Documentation
- [ ] App Directory submission
- [ ] Production deployment

---

## Consequences

### Positive
- Faster development velocity
- Better real-time responsiveness
- Reduced operational burden
- Access to Reddit's latest features

### Negative
- Loss of cross-subreddit global access (can be mitigated by installing in multiple subs)
- Dependency on Reddit's infrastructure
- Learning curve for team on TypeScript/Devvit

### Neutral
- Language change (Python → TypeScript)
- Different testing approach needed

---

## References

- [Devvit Documentation](https://developers.reddit.com/docs/)
- [Reddit API Access Request](https://support.reddithelp.com/hc/en-us/requests/new?ticket_form_id=14868593862164)
- [Devvit Examples](https://github.com/reddit/devvit-examples)
