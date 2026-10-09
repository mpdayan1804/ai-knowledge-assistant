"""
Async demonstration script using HTTPX and AsyncIO.

This script demonstrates async/await patterns for making concurrent HTTP requests.
In a real scenario, this could be used to call external APIs or services asynchronously.
"""

import asyncio
import httpx


async def fetch_url(client: httpx.AsyncClient, url: str) -> dict:
    """
    Fetch a URL asynchronously.

    Args:
        client: HTTPX async client
        url: URL to fetch

    Returns:
        Dictionary with URL and status
    """
    try:
        response = await client.get(url)
        return {
            "url": url,
            "status_code": response.status_code,
            "success": response.status_code == 200
        }
    except Exception as e:
        return {
            "url": url,
            "status_code": None,
            "success": False,
            "error": str(e)
        }


async def main():
    """
    Main async function that demonstrates concurrent HTTP requests.
    """
    print("=== Async HTTP Demo with HTTPX ===\n")

    # List of URLs to fetch concurrently
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/uuid"
    ]

    print(f"Fetching {len(urls)} URLs concurrently...\n")

    # Create async client and make concurrent requests
    async with httpx.AsyncClient(timeout=5.0) as client:
        # Create tasks for all URLs
        tasks = [fetch_url(client, url) for url in urls]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)

    # Print results
    for result in results:
        if result["success"]:
            print(f"✓ {result['url']} - Status: {result['status_code']}")
        else:
            print(f"✗ {result['url']} - Error: {result.get('error', 'Unknown')}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
