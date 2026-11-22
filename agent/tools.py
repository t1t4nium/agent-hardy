"""Tool registry: an @tool decorator plus schema helpers.
Each tool is a function returning a short string. The first line of its
docstring becomes its description. Tools that take arguments declare them
with the @tool(schema=...) parameter, using JSON Schema.
"""

import json

_REGISTRY = {}
_SCHEMAS = {}

def tool(fn=None, *, name=None, schema=None):
    """Decorator: register a function as an agent tool.
    schema is an optional JSON Schema dict describing the parameters.
    """
    def wrap(f):
        tool_name = name or f.__name__
        _REGISTRY[tool_name] = f
        if schema is not None:
            _SCHEMAS[tool_name] = schema
        return f
    if fn is None:
        return wrap
    return wrap(fn)

def _description(fn):
    """First docstring line, used as the tool description."""
    doc = (fn.__doc__ or "").strip().splitlines()
    return doc[0].strip() if doc else ""

def get_tool_schemas():
    """Return the "tools" array expected by OpenAI-compatible servers."""
    return [
        {
            "type": "function",
            "function": {
                "name": name,
                "description": _description(fn),
                "parameters": _SCHEMAS.get(name, {"type": "object", "properties": {}})
            }
        }
        for name, fn in _REGISTRY.items()
    ]

def call_tool(name, arguments):
    """Run a tool by name. arguments is the JSON string sent by the model."""
    fn = _REGISTRY.get(name)
    if fn is None:
        return f"Unknown tool: {name}"
    try:
        args = json.loads(arguments) if isinstance(arguments, str) else (arguments or {})
        return str(fn(**args))
    except Exception as e:
        return f"Tool {name} failed: {e}"
