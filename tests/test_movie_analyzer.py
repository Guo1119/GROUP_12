import pytest
from src.movie_analysis import MovieAnalyzer


def test_movie_type_invalid_input():
    """Ensure movie_type raises error when input is not an integer."""
    analyzer = MovieAnalyzer()
    with pytest.raises(ValueError):
        analyzer.movie_type("ten")


def test_actor_distributions_invalid_input():
    """Ensure actor_distributions raises error when inputs are invalid."""
    analyzer = MovieAnalyzer()
    with pytest.raises(ValueError):
        analyzer.actor_distributions(gender=5, max_height="tall", min_height="short")
