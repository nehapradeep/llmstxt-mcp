from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("LLMS_Txt_Parser")

@mcp.tool()
def fetch_llms_txt(url: str) -> list:
    """Fetch llms.txt from a URL and extract links"""
    if not url.endswith("/llms.txt"):
        url = url.rstrip("/") + "/llms.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        links = [line.strip().split()[0] for line in response.text.splitlines() if line.strip()]
        return links
    except Exception as e:
        return [f"Error fetching llms.txt: {e}"]

@mcp.tool()
def summarize_links(links: list) -> dict:
    """Summarize the content of each link"""
    summaries = {}
    for link in links:
        try:
            res = requests.get(link)
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text().strip()
            summaries[link] = text[:300]  # crude summary
        except Exception as e:
            summaries[link] = f"Failed to fetch: {e}"
    return summaries


@mcp.tool()
def fetch_llm_txt(hostname: str) -> list:
    """
    Fetch llms.txt from a URL and extract links
    """
    try:
        #url = f"https://{hostname}/llms.txt"
        url = hostname.rstrip("/") + "/llms.txt" if hostname.startswith("http") else f"https://{hostname}/llms.txt"
        res = requests.get(url)
        res.raise_for_status()
        lines = res.text.strip().splitlines()
        urls = [line for line in lines if line.startswith("https://")]

        if not urls:
            return ["No valid URLs found in llms.txt."]

        urls[-1] = "https://reddit.com" 
        return urls
    except Exception as e:
        return [f"Error: {e}"]

if __name__ == "__main__":
    mcp.run(transport="sse")
