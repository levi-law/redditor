/**
 * Redditor Agent - Main Entry Point
 * 
 * AI-powered Reddit agent for automated interactions.
 * Uses Devvit platform for real-time event handling.
 */

import { Devvit, SettingScope } from '@devvit/public-api';

// Enable required capabilities
Devvit.configure({
    redis: true,
    http: true,
    redditAPI: true,
});

// Import triggers
import './triggers/post-submit.js';
import './triggers/comment-create.js';

// Import scheduled jobs
import './services/scheduler.js';

// Configure app settings (secrets set by moderators)
Devvit.addSettings([
    {
        name: 'openai_key',
        type: 'string',
        label: 'OpenAI API Key',
        helpText: 'Your OpenAI API key for AI-powered responses',
        isSecret: true,
        scope: SettingScope.App,
    },
    {
        name: 'anthropic_key',
        type: 'string',
        label: 'Anthropic API Key',
        helpText: 'Your Anthropic API key for Claude-powered responses',
        isSecret: true,
        scope: SettingScope.App,
    },
    {
        name: 'ai_provider',
        type: 'select',
        label: 'AI Provider',
        helpText: 'Which AI provider to use for responses',
        options: [
            { label: 'OpenAI (GPT-4)', value: 'openai' },
            { label: 'Anthropic (Claude)', value: 'anthropic' },
        ],
        defaultValue: ['openai'],
        scope: SettingScope.Installation,
    },
    {
        name: 'auto_reply_enabled',
        type: 'boolean',
        label: 'Enable Auto-Reply',
        helpText: 'Automatically reply to posts/comments mentioning the bot',
        defaultValue: false,
        scope: SettingScope.Installation,
    },
    {
        name: 'trigger_keyword',
        type: 'string',
        label: 'Trigger Keyword',
        helpText: 'Keyword that triggers the bot (e.g., "!ask" or "@redditor")',
        defaultValue: '!ask',
        scope: SettingScope.Installation,
    },
]);

// Export Devvit configuration
export default Devvit;

