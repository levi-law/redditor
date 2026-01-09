/**
 * Scheduler Service
 * 
 * Handles scheduled/recurring background jobs.
 */

import { Devvit } from '@devvit/public-api';

// Daily stats summary job
Devvit.addSchedulerJob({
    name: 'daily-stats-summary',
    onRun: async (_event, context) => {
        try {
            const stats = await context.redis.hGetAll('stats');

            console.log('Daily Stats Summary:');
            console.log(`  Posts processed: ${stats.posts_processed || 0}`);
            console.log(`  Comments processed: ${stats.comments_processed || 0}`);

            // Could send a modmail summary here
            // await context.reddit.sendPrivateMessageAsSubreddit({...});

        } catch (error) {
            console.error('Error in daily-stats-summary:', error);
        }
    },
});

// Health check job
Devvit.addSchedulerJob({
    name: 'health-check',
    onRun: async (_event, context) => {
        try {
            // Ping Redis to ensure connectivity
            await context.redis.set('health-check', Date.now().toString());
            console.log('Health check passed');
        } catch (error) {
            console.error('Health check failed:', error);
        }
    },
});

// App install trigger - set up scheduled jobs
Devvit.addTrigger({
    event: 'AppInstall',
    onEvent: async (_event, context) => {
        try {
            // Schedule daily stats at 9 AM UTC
            await context.scheduler.runJob({
                name: 'daily-stats-summary',
                cron: '0 9 * * *',
            });

            // Schedule health check every 5 minutes
            await context.scheduler.runJob({
                name: 'health-check',
                cron: '*/5 * * * *',
            });

            console.log('Scheduled jobs set up successfully');

            // Initialize stats
            await context.redis.hSet('stats', {
                posts_processed: '0',
                comments_processed: '0',
                install_date: new Date().toISOString(),
            });

        } catch (error) {
            console.error('Error setting up scheduled jobs:', error);
        }
    },
});
