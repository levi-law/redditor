/**
 * AI Service
 * 
 * Provides AI-powered response generation using OpenAI or Anthropic.
 */

import { TriggerContext } from '@devvit/public-api';

interface ChatMessage {
    role: 'system' | 'user' | 'assistant';
    content: string;
}

interface OpenAIResponse {
    choices: Array<{
        message: {
            content: string;
        };
    }>;
}

interface AnthropicResponse {
    content: Array<{
        text: string;
    }>;
}

const SYSTEM_PROMPT = `You are a helpful Reddit assistant. Your responses should be:
- Concise and to the point (Reddit users prefer shorter responses)
- Friendly and conversational
- Accurate and factual
- Include markdown formatting where appropriate
- Respectful of Reddit culture and community guidelines

If you don't know something, say so. Don't make things up.`;

/**
 * Generate an AI response using the configured provider
 */
export async function generateAIResponse(
    context: TriggerContext,
    question: string
): Promise<string> {
    const provider = await context.settings.get('ai_provider') as string[] || ['openai'];
    const selectedProvider = provider[0] || 'openai';

    try {
        if (selectedProvider === 'anthropic') {
            return await generateAnthropicResponse(context, question);
        } else {
            return await generateOpenAIResponse(context, question);
        }
    } catch (error) {
        console.error(`AI generation error (${selectedProvider}):`, error);
        return "I'm sorry, I encountered an error processing your request. Please try again later.";
    }
}

/**
 * Generate response using OpenAI
 */
async function generateOpenAIResponse(
    context: TriggerContext,
    question: string
): Promise<string> {
    const apiKey = await context.settings.get('openai_key') as string;

    if (!apiKey) {
        return "OpenAI API key not configured. Please contact the subreddit moderators.";
    }

    const messages: ChatMessage[] = [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: question },
    ];

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: 'gpt-4-turbo-preview',
            messages,
            max_tokens: 500,
            temperature: 0.7,
        }),
    });

    if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.status}`);
    }

    const data = await response.json() as OpenAIResponse;
    return data.choices[0]?.message?.content || "Unable to generate response.";
}

/**
 * Generate response using Anthropic Claude
 */
async function generateAnthropicResponse(
    context: TriggerContext,
    question: string
): Promise<string> {
    const apiKey = await context.settings.get('anthropic_key') as string;

    if (!apiKey) {
        return "Anthropic API key not configured. Please contact the subreddit moderators.";
    }

    const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            model: 'claude-3-sonnet-20240229',
            max_tokens: 500,
            system: SYSTEM_PROMPT,
            messages: [
                { role: 'user', content: question },
            ],
        }),
    });

    if (!response.ok) {
        throw new Error(`Anthropic API error: ${response.status}`);
    }

    const data = await response.json() as AnthropicResponse;
    return data.content[0]?.text || "Unable to generate response.";
}

/**
 * Store conversation in Redis for context
 * Uses sorted sets with timestamp as score for ordering
 */
export async function storeConversation(
    context: TriggerContext,
    userId: string,
    question: string,
    answer: string
): Promise<void> {
    const key = `conversation:${userId}`;
    const timestamp = Date.now();
    const conversation = JSON.stringify({
        timestamp,
        question,
        answer,
    });

    // Store conversation with timestamp as score
    await context.redis.zAdd(key, { score: timestamp, member: conversation });

    // Keep only latest 5 (trim older entries)
    const count = await context.redis.zCard(key);
    if (count > 5) {
        await context.redis.zRemRangeByRank(key, 0, count - 6);
    }
}

/**
 * Retrieve conversation history from Redis
 */
export async function getConversationHistory(
    context: TriggerContext,
    userId: string
): Promise<Array<{ question: string; answer: string }>> {
    const key = `conversation:${userId}`;
    const items = await context.redis.zRange(key, 0, 4);

    return items.map((item: { member: string }) => JSON.parse(item.member));
}
