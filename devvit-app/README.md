# Redditor Agent - Devvit App

This is the Devvit version of the Redditor AI agent.

## Prerequisites

- Node.js >= 22.2.0
- Devvit CLI installed: `npm install -g devvit`
- Reddit account

## Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Login to Devvit**
   ```bash
   devvit login
   ```

3. **Develop locally**
   ```bash
   npm run dev
   ```

4. **Upload to Reddit**
   ```bash
   npm run upload
   ```

## Project Structure

```
devvit-app/
├── src/
│   ├── main.ts          # App entry point
│   ├── triggers/        # Event handlers
│   ├── services/        # AI and utility services
│   └── types/           # TypeScript types
├── devvit.yaml          # Devvit configuration
├── package.json
└── tsconfig.json
```

## Features

- **AI-Powered Responses**: Uses OpenAI/Anthropic for intelligent replies
- **Real-time Triggers**: Responds instantly to posts and comments
- **Scheduled Tasks**: Runs periodic community engagement tasks
- **Data Persistence**: Stores conversation history in Redis

## Configuration

Set API keys in your subreddit's app settings after installation:
- `openai_key` - OpenAI API key
- `anthropic_key` - Anthropic API key
