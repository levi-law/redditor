/**
 * Comment Create Trigger
 * 
 * Handles new comment creation in the subreddit.
 * Responds to comments that mention the bot or use trigger keyword.
 */

import { Devvit, TriggerContext } from '@devvit/public-api';
import { generateAIResponse } from '../services/ai.js';

Devvit.addTrigger({
    event: 'CommentCreate',
    onEvent: async (event, context: TriggerContext) => {
        try {
            // Check if auto-reply is enabled
            const autoReplyEnabled = await context.settings.get('auto_reply_enabled');
            if (!autoReplyEnabled) {
                return;
            }

            // Get the comment details
            const comment = event.comment;
            if (!comment) {
                console.log('Comment not found in event');
                return;
            }

            // Skip if it's our own comment (avoid infinite loops)
            const currentUser = await context.reddit.getCurrentUser();
            if (comment.author === currentUser?.username) {
                return;
            }

            // Get trigger keyword
            const triggerKeyword = await context.settings.get('trigger_keyword') as string || '!ask';

            // Check if comment contains trigger keyword
            if (!comment.body.toLowerCase().includes(triggerKeyword.toLowerCase())) {
                return;
            }

            // Extract the question (remove trigger keyword)
            const question = comment.body.replace(new RegExp(triggerKeyword, 'gi'), '').trim();

            if (!question) {
                await context.reddit.submitComment({
                    id: comment.id,
                    text: "Please provide a question after the trigger keyword!",
                });
                return;
            }

            // Generate AI response
            const aiResponse = await generateAIResponse(context, question);

            // Reply to the comment
            await context.reddit.submitComment({
                id: comment.id,
                text: aiResponse,
            });

            console.log(`Replied to comment ${comment.id} with AI response`);

            // Store in Redis for analytics
            await context.redis.hIncrBy('stats', 'comments_processed', 1);

        } catch (error) {
            console.error('Error in CommentCreate trigger:', error);
        }
    },
});
