"""Reddit API client wrapping PRAW.

Provides a high-level interface to Reddit's API with authentication,
rate limiting, and common operations.
"""

import time
from typing import Iterator, Optional, Any
import logging

import praw
from praw.models import Submission, Comment, Subreddit

logger = logging.getLogger(__name__)


class RedditClient:
    """Reddit API client using PRAW.
    
    Provides authenticated access to Reddit with rate limiting
    and convenient methods for common operations.
    
    Args:
        client_id: Reddit OAuth2 client ID
        client_secret: Reddit OAuth2 client secret
        user_agent: User agent string for API requests
        username: Optional Reddit username for authenticated actions
        password: Optional Reddit password for authenticated actions
    
    Raises:
        ValueError: If client_id or client_secret are not provided
    """
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        if not client_id:
            raise ValueError("client_id is required")
        if not client_secret:
            raise ValueError("client_secret is required")
        
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_agent = user_agent
        self._username = username
        self._password = password
        
        # Initialize PRAW
        self._reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )
        
        # Rate limiting state
        self._last_request_time: float = 0
        self._min_request_interval: float = 1.0  # seconds
    
    @property
    def authenticated(self) -> bool:
        """Check if the client has valid authentication."""
        try:
            return self._reddit.user.me() is not None
        except Exception:
            return False
    
    @property
    def is_authenticated(self) -> bool:
        """Alias for authenticated property."""
        return self.authenticated
    
    @property
    def requests_remaining(self) -> Optional[int]:
        """Get remaining API requests if available."""
        try:
            return self._reddit.auth.limits.get("remaining")
        except Exception:
            return None
    
    @property
    def rate_limit(self) -> dict:
        """Get current rate limit information."""
        try:
            limits = self._reddit.auth.limits
            return {
                "remaining": limits.get("remaining"),
                "used": limits.get("used"),
                "reset_timestamp": limits.get("reset_timestamp"),
            }
        except Exception:
            return {}
    
    def _respect_rate_limit(self) -> None:
        """Ensure minimum time between requests."""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self._min_request_interval:
            time.sleep(self._min_request_interval - elapsed)
        self._last_request_time = time.time()
    
    def get_subreddit(self, name: str) -> Subreddit:
        """Get a subreddit by name.
        
        Args:
            name: Subreddit name (without r/ prefix)
            
        Returns:
            PRAW Subreddit object
        """
        self._respect_rate_limit()
        return self._reddit.subreddit(name)
    
    def get_posts(
        self,
        subreddit: str,
        sort: str = "hot",
        limit: int = 10,
        time_filter: str = "all",
    ) -> Iterator[Submission]:
        """Get posts from a subreddit.
        
        Args:
            subreddit: Subreddit name
            sort: Sorting method (hot, new, top, rising, controversial)
            limit: Maximum number of posts to return
            time_filter: Time filter for top/controversial (hour, day, week, month, year, all)
            
        Yields:
            PRAW Submission objects
        """
        self._respect_rate_limit()
        sub = self._reddit.subreddit(subreddit)
        
        if sort == "hot":
            posts = sub.hot(limit=limit)
        elif sort == "new":
            posts = sub.new(limit=limit)
        elif sort == "top":
            posts = sub.top(time_filter=time_filter, limit=limit)
        elif sort == "rising":
            posts = sub.rising(limit=limit)
        elif sort == "controversial":
            posts = sub.controversial(time_filter=time_filter, limit=limit)
        else:
            posts = sub.hot(limit=limit)
        
        yield from posts
    
    def get_post(self, post_id: str) -> Submission:
        """Get a specific post by ID.
        
        Args:
            post_id: Reddit post ID
            
        Returns:
            PRAW Submission object
        """
        self._respect_rate_limit()
        return self._reddit.submission(id=post_id)
    
    def get_comments(
        self,
        post_id: str,
        limit: Optional[int] = None,
        sort: str = "best",
    ) -> Iterator[Comment]:
        """Get comments from a post.
        
        Args:
            post_id: Reddit post ID
            limit: Maximum number of comments (None for all)
            sort: Comment sort order (best, new, top, controversial, old, qa)
            
        Yields:
            PRAW Comment objects
        """
        self._respect_rate_limit()
        submission = self._reddit.submission(id=post_id)
        submission.comment_sort = sort
        
        if limit:
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list()[:limit]:
                yield comment
        else:
            submission.comments.replace_more(limit=0)
            yield from submission.comments.list()
    
    def search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        sort: str = "relevance",
        limit: int = 25,
    ) -> Iterator[Submission]:
        """Search for posts.
        
        Args:
            query: Search query string
            subreddit: Optional subreddit to search within
            sort: Sort method (relevance, hot, top, new, comments)
            limit: Maximum results
            
        Yields:
            PRAW Submission objects
        """
        self._respect_rate_limit()
        
        if subreddit:
            sub = self._reddit.subreddit(subreddit)
            results = sub.search(query, sort=sort, limit=limit)
        else:
            results = self._reddit.subreddit("all").search(query, sort=sort, limit=limit)
        
        yield from results
    
    def submit_comment(self, post_id: str, body: str) -> Comment:
        """Submit a comment to a post.
        
        Args:
            post_id: Reddit post ID
            body: Comment text
            
        Returns:
            Created PRAW Comment object
        """
        self._respect_rate_limit()
        submission = self._reddit.submission(id=post_id)
        return submission.reply(body)
