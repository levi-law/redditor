# Devvit Reddit API Reference

> **Full Reference**: https://developers.reddit.com/docs/api/redditapi/RedditAPIClient/

## RedditAPIClient Methods

Access via `context.reddit` in any Devvit handler.

---

## Posts

### Reading Posts
```typescript
// Get hot posts from current subreddit
const posts = await context.reddit.getHotPosts({
  subredditName: 'askreddit',
  limit: 25,
  pageSize: 10
});

// Get new posts
const newPosts = await context.reddit.getNewPosts({ subredditName, limit: 10 });

// Get top posts
const topPosts = await context.reddit.getTopPosts({ 
  subredditName, 
  timeframe: 'day',  // hour, day, week, month, year, all
  limit: 10 
});

// Get single post by ID
const post = await context.reddit.getPostById(postId);
```

### Creating Posts
```typescript
// Text post
await context.reddit.submitPost({
  subredditName: 'test',
  title: 'Hello World',
  text: 'This is the body'
});

// Link post
await context.reddit.submitPost({
  subredditName: 'test',
  title: 'Check this out',
  url: 'https://example.com'
});
```

---

## Comments

### Reading Comments
```typescript
// Get comments on a post
const comments = await context.reddit.getComments({
  postId: 't3_abc123',
  limit: 100,
  sort: 'best'  // best, top, new, controversial, old, qa
});

// Get single comment
const comment = await context.reddit.getCommentById(commentId);
```

### Creating Comments
```typescript
// Reply to a post
await context.reddit.submitComment({
  id: 't3_abc123',  // Post ID
  text: 'Great post!'
});

// Reply to a comment
await context.reddit.submitComment({
  id: 't1_xyz789',  // Comment ID
  text: 'I agree!'
});
```

---

## Private Messages

### Sending Messages
```typescript
// Send as yourself (the app's account)
await context.reddit.sendPrivateMessage({
  to: 'username',
  subject: 'Hello',
  text: 'This is a message'
});

// Send as the subreddit (requires mod permissions)
await context.reddit.sendPrivateMessageAsSubreddit({
  fromSubredditName: 'mysubreddit',
  to: 'username',
  subject: 'Mod Notice',
  text: 'You have been warned'
});
```

### Reading Messages
```typescript
const messages = await context.reddit.getMessages({
  type: 'inbox',  // inbox, unread, sent
  limit: 25
});
```

---

## Users

```typescript
// Get current user (the one who triggered the event)
const user = await context.reddit.getCurrentUser();

// Get user by ID
const user = await context.reddit.getUserById('t2_abc123');

// Get user by username
const user = await context.reddit.getUserByUsername('spez');
```

---

## Subreddits

```typescript
// Get current subreddit (where app is installed)
const subreddit = await context.reddit.getCurrentSubreddit();

// Get subreddit by name
const subreddit = await context.reddit.getSubredditByName('programming');

// Get subreddit info
const info = await context.reddit.getSubredditInfoByName('askreddit');
```

---

## Moderation

```typescript
// Remove content
await context.reddit.remove(thingId, isSpam);

// Approve content
await context.reddit.approve(thingId);

// Ban user
await context.reddit.banUser({
  subredditName: 'mysubreddit',
  username: 'baduser',
  duration: 7,  // days, omit for permanent
  reason: 'Rule violation',
  note: 'Internal mod note'
});

// Unban user
await context.reddit.unbanUser({
  subredditName: 'mysubreddit',
  username: 'forgiven_user'
});

// Set flair
await context.reddit.setPostFlair({
  postId: 't3_abc123',
  subredditName: 'mysubreddit',
  flairTemplateId: 'template-id'
});
```

---

## Voting

```typescript
// Upvote
await context.reddit.upvote(thingId);

// Downvote
await context.reddit.downvote(thingId);

// Remove vote
await context.reddit.removeVote(thingId);
```

---

## Flairs

```typescript
// Get user flair templates
const flairs = await context.reddit.getUserFlairTemplates(subredditName);

// Get post flair templates
const flairs = await context.reddit.getPostFlairTemplates(subredditName);

// Set user flair
await context.reddit.setUserFlair({
  subredditName: 'mysubreddit',
  username: 'someuser',
  text: 'Helpful Member',
  cssClass: 'helpful'
});
```

---

## Widgets (Sidebar)

```typescript
// Get subreddit widgets
const widgets = await context.reddit.getWidgets(subredditName);

// Add text widget
await context.reddit.addTextWidget({
  subredditName: 'mysubreddit',
  name: 'Welcome',
  text: 'Welcome to our community!'
});
```

---

## Common Patterns

### Auto-reply to new posts
```typescript
Devvit.addTrigger({
  event: 'PostSubmit',
  onEvent: async (event, context) => {
    await context.reddit.submitComment({
      id: event.postId,
      text: 'Thank you for your submission! Please read our rules.'
    });
  }
});
```

### Keyword monitoring
```typescript
Devvit.addTrigger({
  event: 'CommentCreate',
  onEvent: async (event, context) => {
    const comment = await context.reddit.getCommentById(event.commentId);
    if (comment.body.toLowerCase().includes('help')) {
      await context.reddit.submitComment({
        id: comment.id,
        text: 'Need help? Check our FAQ: /r/subreddit/wiki/faq'
      });
    }
  }
});
```

### AI-powered responses
```typescript
Devvit.addTrigger({
  event: 'CommentCreate',
  onEvent: async (event, context) => {
    if (event.comment.body.includes('!ask')) {
      const question = event.comment.body.replace('!ask', '').trim();
      
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${await context.settings.get('openai_key')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'gpt-4',
          messages: [{ role: 'user', content: question }]
        })
      });
      
      const data = await response.json();
      await context.reddit.submitComment({
        id: event.commentId,
        text: data.choices[0].message.content
      });
    }
  }
});
```
