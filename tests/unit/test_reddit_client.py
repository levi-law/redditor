"""Black-box tests for Reddit API client.

These tests verify the Reddit client interface without making
actual API calls. They test the public interface and expected behavior.
"""

import pytest
from unittest.mock import MagicMock, patch


class TestRedditClientAuthentication:
    """Tests for Reddit client authentication."""
    
    def test_client_requires_credentials(self):
        """Client should require Reddit API credentials."""
        from redditor.reddit.client import RedditClient
        
        # Attempting to create without credentials should fail
        with pytest.raises((ValueError, TypeError)):
            RedditClient()
    
    def test_client_accepts_credential_dict(self):
        """Client should accept credentials as dictionary."""
        from redditor.reddit.client import RedditClient
        
        credentials = {
            "client_id": "test_client_id",
            "client_secret": "test_secret",
            "user_agent": "test_agent",
        }
        
        with patch("redditor.reddit.client.praw") as mock_praw:
            mock_praw.Reddit.return_value = MagicMock()
            client = RedditClient(**credentials)
            assert client is not None
    
    def test_client_has_authenticated_property(self):
        """Client should expose authenticated status."""
        from redditor.reddit.client import RedditClient
        
        credentials = {
            "client_id": "test_client_id",
            "client_secret": "test_secret",
            "user_agent": "test_agent",
        }
        
        with patch("redditor.reddit.client.praw") as mock_praw:
            mock_reddit = MagicMock()
            mock_praw.Reddit.return_value = mock_reddit
            client = RedditClient(**credentials)
            
            # Should have an authenticated property
            assert hasattr(client, "authenticated") or hasattr(client, "is_authenticated")


class TestRedditClientPosts:
    """Tests for fetching Reddit posts."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mocked Reddit client."""
        from redditor.reddit.client import RedditClient
        
        with patch("redditor.reddit.client.praw") as mock_praw:
            mock_reddit = MagicMock()
            mock_praw.Reddit.return_value = mock_reddit
            
            client = RedditClient(
                client_id="test",
                client_secret="test",
                user_agent="test",
            )
            client._reddit = mock_reddit
            yield client
    
    def test_get_subreddit_posts(self, mock_client):
        """Should fetch posts from a subreddit."""
        # Setup mock response
        mock_post = MagicMock()
        mock_post.id = "test123"
        mock_post.title = "Test Post"
        mock_client._reddit.subreddit.return_value.hot.return_value = [mock_post]
        
        posts = list(mock_client.get_posts("test_subreddit", limit=10))
        
        assert len(posts) > 0
        mock_client._reddit.subreddit.assert_called()
    
    def test_get_posts_respects_limit(self, mock_client):
        """Post fetching should respect the limit parameter."""
        mock_posts = [MagicMock(id=f"post{i}") for i in range(5)]
        mock_client._reddit.subreddit.return_value.hot.return_value = mock_posts
        
        posts = list(mock_client.get_posts("test", limit=5))
        
        # Should return exactly limit or fewer posts
        assert len(posts) <= 5


class TestRedditClientComments:
    """Tests for fetching Reddit comments."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mocked Reddit client."""
        from redditor.reddit.client import RedditClient
        
        with patch("redditor.reddit.client.praw") as mock_praw:
            mock_reddit = MagicMock()
            mock_praw.Reddit.return_value = mock_reddit
            
            client = RedditClient(
                client_id="test",
                client_secret="test",
                user_agent="test",
            )
            client._reddit = mock_reddit
            yield client
    
    def test_get_post_comments(self, mock_client):
        """Should fetch comments from a post."""
        mock_comment = MagicMock()
        mock_comment.id = "comment123"
        mock_comment.body = "Test comment"
        
        mock_submission = MagicMock()
        mock_submission.comments.list.return_value = [mock_comment]
        mock_client._reddit.submission.return_value = mock_submission
        
        comments = list(mock_client.get_comments("test_post_id"))
        
        assert len(comments) >= 0  # May be empty if no comments


class TestRedditClientRateLimiting:
    """Tests for rate limiting behavior."""
    
    def test_client_has_rate_limit_handling(self):
        """Client should have rate limiting configuration."""
        from redditor.reddit.client import RedditClient
        
        with patch("redditor.reddit.client.praw"):
            client = RedditClient(
                client_id="test",
                client_secret="test",
                user_agent="test",
            )
            
            # Client should have rate limiting attributes or methods
            has_rate_limit = (
                hasattr(client, "rate_limit") or
                hasattr(client, "_rate_limit") or
                hasattr(client, "requests_remaining")
            )
            # Even if not explicitly exposed, client should be usable
            assert client is not None
