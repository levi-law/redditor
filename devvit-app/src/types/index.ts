/**
 * Common TypeScript types for Redditor Agent
 */

export interface ConversationEntry {
    timestamp: number;
    question: string;
    answer: string;
}

export interface AppStats {
    posts_processed: number;
    comments_processed: number;
    install_date: string;
}

export type AIProvider = 'openai' | 'anthropic';

export interface AIConfig {
    provider: AIProvider;
    model: string;
    maxTokens: number;
    temperature: number;
}

export const DEFAULT_AI_CONFIG: AIConfig = {
    provider: 'openai',
    model: 'gpt-4-turbo-preview',
    maxTokens: 500,
    temperature: 0.7,
};
