# leave_mcp_server.py
from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import List, Dict

mcp = FastMCP("LeaveManagement")

# In-memory leave request store
leave_requests: List[Dict] = []

@mcp.tool()
def apply_leave(name: str, start_date: str, end_date: str, reason: str) -> str:
    """Submit a leave request"""
    leave = {
        "name": name,
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
        "status": "Pending",
        "timestamp": datetime.now().isoformat()
    }
    leave_requests.append(leave)
    return f"Leave request submitted for {name} from {start_date} to {end_date}."

@mcp.tool()
def approve_leave(index: int) -> str:
    """Approve a leave request by index"""
    if 0 <= index < len(leave_requests):
        leave_requests[index]["status"] = "Approved"
        return f"Leave request #{index} approved."
    return "Invalid index."

@mcp.tool()
def reject_leave(index: int) -> str:
    """Reject a leave request by index"""
    if 0 <= index < len(leave_requests):
        leave_requests[index]["status"] = "Rejected"
        return f"Leave request #{index} rejected."
    return "Invalid index."

@mcp.tool()
def list_leaves() -> List[Dict]:
    """List all leave requests"""
    return leave_requests

# --- Tool: Get In-Memory Cache (Demo) ---
memory_cache = {}

@mcp.tool()
def get_memory(key: str) -> str:
    """Get value from memory cache"""
    return memory_cache.get(key, "No data found.")

@mcp.tool()
def set_memory(key: str, value: str) -> str:
    """Store a key-value in memory cache"""
    memory_cache[key] = value
    return f"Stored '{key}': '{value}'"

@mcp.resource("leave-status://{name}")
def leave_status(name: str) -> str:
    """Get the status of leave requests for a user"""
    user_leaves = [lr for lr in leave_requests if lr["name"] == name]
    if not user_leaves:
        return "No leave requests found."
    return "\n".join(
        f"#{i}: {lr['start_date']} to {lr['end_date']} — {lr['status']}"
        for i, lr in enumerate(user_leaves)
    )


# @mcp.resource("resources/list")
# def list_resources():
#     """Get the status of leave requests for a user"""
#     return {
#         "uri": "https://example.com/mydoc",
#         "name": "Example Document",
#         "description": "This is a sample test document.",
#         "mimeType": "text/html"
#     }

####
# {
#   uri: string;           // Unique identifier for the resource
#   name: string;          // Human-readable name
#   description?: string;  // Optional description
#   mimeType?: string;     // Optional MIME type
# }

if __name__ == "__main__":
    mcp.run(transport="sse")

