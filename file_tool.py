from fastmcp import FastMCP
import sys
import logging
import os

logger = logging.getLogger('FileTool')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("FileTool")

# Add a file tool
@mcp.tool()
def file_tool(action: str, **kwargs) -> dict:
    """For file operations. Actions: 'read' (read file content), 'write' (write content to file), 'list' (list files in directory), 'exists' (check if file exists)."""
    if action == 'read':
        # Read file content
        file_path = kwargs.get('file_path')
        if not file_path:
            return {"success": False, "error": "Missing file_path parameter"}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Reading file: {file_path}")
            return {"success": True, "result": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    elif action == 'write':
        # Write content to file
        file_path = kwargs.get('file_path')
        content = kwargs.get('content')
        if not file_path:
            return {"success": False, "error": "Missing file_path parameter"}
        if content is None:
            return {"success": False, "error": "Missing content parameter"}
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Writing to file: {file_path}")
            return {"success": True, "result": "File written successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    elif action == 'list':
        # List files in directory
        directory = kwargs.get('directory', '.')
        try:
            files = os.listdir(directory)
            logger.info(f"Listing files in directory: {directory}")
            return {"success": True, "result": files}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    elif action == 'exists':
        # Check if file exists
        file_path = kwargs.get('file_path')
        if not file_path:
            return {"success": False, "error": "Missing file_path parameter"}
        try:
            exists = os.path.exists(file_path)
            logger.info(f"Checking if file exists: {file_path} -> {exists}")
            return {"success": True, "result": exists}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    else:
        return {"success": False, "error": f"Unknown action: {action}"}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")