from fastmcp import FastMCP
import sys
import logging
import psutil

logger = logging.getLogger('SystemMonitor')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Try to import GPU monitoring library
try:
    import pynvml
    pynvml.nvmlInit()
    gpu_available = True
except ImportError:
    gpu_available = False
    logger.warning("pynvml library not found. GPU monitoring will be disabled.")
except Exception as e:
    gpu_available = False
    logger.warning(f"Failed to initialize GPU monitoring: {e}")

# Create an MCP server
mcp = FastMCP("SystemMonitor")

# Add a system monitor tool
@mcp.tool()
def system_monitor() -> dict:
    """Monitor system performance metrics including memory, CPU, disk, and GPU usage percentages."""
    try:
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Get disk usage (Windows用C盘，Linux用根目录)
        if sys.platform == 'win32':
            disk_path = 'C:\\'
        else:
            disk_path = '/'
        disk = psutil.disk_usage(disk_path)
        disk_usage = disk.percent
        
        # Get GPU usage if available
        gpu_usage = None
        if gpu_available:
            try:
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count > 0:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    gpu_usage = utilization.gpu
            except Exception as e:
                logger.warning(f"Error getting GPU usage: {e}")
        
        # Build result
        result = {
            "memory_usage_percent": memory_usage,
            "cpu_usage_percent": cpu_usage,
            "disk_usage_percent": disk_usage,
            "gpu_usage_percent": gpu_usage,
            "timestamp": psutil.boot_time()
        }
        
        logger.info(f"System performance: {result}")
        return {"success": True, "result": result}
        
    except Exception as e:
        logger.error(f"Error monitoring system: {e}")
        return {"success": False, "error": str(e)}

# Start the server - 纯 stdio 模式，由 mcp_pipe 管理 WebSocket 连接
if __name__ == "__main__":
    mcp.run(transport="stdio")