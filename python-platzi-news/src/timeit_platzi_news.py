import timeit

from platzi_news.analysis.analyzer import (
    find_duplicate_titles,
    find_duplicate_titles_improved,
)
from platzi_news.core.models import Article


def create_test_articles(n: int) -> list[Article]:
    """Create a list of articles with some duplicate titles for testing."""
    return [
        Article(
            title=f"Title {i % (n // 10) if n > 10 else i}",
            description=f"Description for article {i}",
            url=f"https://example.com/article/{i}",
        )
        for i in range(n)
    ]


def test_performance() -> None:
    """Test and display performance comparison
    between original and improved find_duplicate_titles."""
    sizes = [100, 200, 2000, 20000]

    print("Comparison: find_duplicate_titles vs find_duplicate_titles_improved")
    print("Size\tOriginal (O(n^2))\tImproved (O(n))\tSpeedup\tDuplicates")
    print("-" * 80)

    for size in sizes:
        articles = create_test_articles(size)

        time_original = timeit.timeit(
            lambda: find_duplicate_titles(articles),
            number=1,
        )
        time_improved = timeit.timeit(
            lambda: find_duplicate_titles_improved(articles),
            number=1,
        )

        # Get duplicates count (should be same for both)
        duplicates = find_duplicate_titles(articles)
        speedup = time_original / time_improved if time_improved > 0 else float("inf")

        print(
            f"{size}\t{time_original:.6f}\t\t{time_improved:.6f}\t{speedup:.1f}x\t{len(duplicates)}"
        )


if __name__ == "__main__":
    test_performance()
