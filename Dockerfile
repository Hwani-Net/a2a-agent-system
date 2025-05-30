FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Set environment variables for MCP server
ENV PYTHONPATH=/app
ENV MCP_MODE=server
ENV PYTHONUNBUFFERED=1

# Expose port (though MCP typically uses STDIO)
EXPOSE 8000

# Set entrypoint to MCP server
ENTRYPOINT ["python", "mcp_server.py"] 