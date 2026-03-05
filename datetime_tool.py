from fastmcp import FastMCP
import sys
import logging
from datetime import datetime, timedelta
import time

logger = logging.getLogger('DateTimeTool')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Create an MCP server
mcp = FastMCP("DateTimeTool")

# Add a datetime tool
@mcp.tool()
def datetime_tool(action: str, **kwargs) -> dict:
    """For date and time operations. Actions: 'now' (get current time), 'format' (format datetime), 'add' (add time delta), 'diff' (calculate difference between two dates)."""
    if action == 'now':
        # Get current time
        now = datetime.now()
        result = {
            "datetime": now.isoformat(),
            "date": now.date().isoformat(),
            "time": now.time().isoformat(),
            "timestamp": time.time()
        }
        logger.info(f"Getting current time: {result}")
        return {"success": True, "result": result}
    
    elif action == 'format':
        # Format datetime
        dt_str = kwargs.get('datetime')
        format_str = kwargs.get('format', '%Y-%m-%d %H:%M:%S')
        if not dt_str:
            return {"success": False, "error": "Missing datetime parameter"}
        try:
            dt = datetime.fromisoformat(dt_str)
            formatted = dt.strftime(format_str)
            logger.info(f"Formatting datetime {dt_str} with format {format_str}: {formatted}")
            return {"success": True, "result": formatted}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    elif action == 'add':
        # Add time delta
        dt_str = kwargs.get('datetime', datetime.now().isoformat())
        days = kwargs.get('days', 0)
        hours = kwargs.get('hours', 0)
        minutes = kwargs.get('minutes', 0)
        seconds = kwargs.get('seconds', 0)
        try:
            dt = datetime.fromisoformat(dt_str)
            delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            result = (dt + delta).isoformat()
            logger.info(f"Adding delta to {dt_str}: {result}")
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    elif action == 'diff':
        # Calculate difference between two dates
        dt1_str = kwargs.get('datetime1')
        dt2_str = kwargs.get('datetime2', datetime.now().isoformat())
        if not dt1_str:
            return {"success": False, "error": "Missing datetime1 parameter"}
        try:
            dt1 = datetime.fromisoformat(dt1_str)
            dt2 = datetime.fromisoformat(dt2_str)
            delta = dt2 - dt1
            result = {
                "days": delta.days,
                "seconds": delta.seconds,
                "total_seconds": delta.total_seconds()
            }
            logger.info(f"Calculating difference between {dt1_str} and {dt2_str}: {result}")
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    else:
        return {"success": False, "error": f"Unknown action: {action}"}

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")