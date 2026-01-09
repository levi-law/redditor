/**
 * Post Submit Trigger
 * 
 * Handles new post submissions in the subreddit.
 * Can provide AI-generated welcome messages or post analysis.
 */

import { Devvit, TriggerContext } from '@devvit/public-api';
import { generateAIResponse } from '../services/ai.js';

Devvit.addTrigger({
    event: 'PostSubmit',
    onEvent: async (event, context: TriggerContext) => {
        try {
            // Check if auto-reply is enabled
            const autoReplyEnabled = await context.settings.get('auto_reply_enabled');
            if (!autoReplyEnabled) {
                return;
            }

            // Get the post details
            const post = event.post;
            if (!post) {
                console.log('Post not found in event');
                return;
            }

            // Skip if it's our own post (avoid infinite loops)
            const currentUser = await context.reddit.getCurrentUser();
            // PostV2 has authorId, get user to compare
            if (post.authorId === currentUser?.id) {
                return;
            }

            // Get trigger keyword
            const triggerKeyword = await context.settings.get('trigger_keyword') as string || '!ask';

            // Check if post title or body contains trigger keyword
            const postContent = `${post.title} ${post.selftext || ''}`;
            if (!postContent.toLowerCase().includes(triggerKeyword.toLowerCase())) {
                return;
            }

            // Generate AI response
            const question = postContent.replace(new RegExp(triggerKeyword, 'gi'), '').trim();
            const aiResponse = await generateAIResponse(context, question);

            // Post the response as a comment
            await context.reddit.submitComment({
                id: post.id,
                text: aiResponse,
            });

            console.log(`Replied to post ${post.id} with AI response`);

            // Store in Redis for analytics
            await context.redis.hIncrBy('stats', 'posts_processed', 1);

        } catch (error) {
            console.error('Error in PostSubmit trigger:', error);
        }
    },
});
