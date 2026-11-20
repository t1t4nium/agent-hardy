"""Tool registry: an @tool decorator plus prompt help.

Each tool is a no-argument function returning a short string. The
first line of its docstring becomes its description in the system
prompt.
"""
_REGISTRY = {}

def tool(fn=None, *, name=None):
    """Decorator: register a function as an agent tool."""
    def wrap(f):
        tool_name = name or f.__name__
        _REGISTRY[tool_name] = f
        f._tool_name = tool_name
        return f
    if fn is None:
        return wrap
    return wrap(fn)

def get_tools():
    """Return a copy of the registry {name: function}."""
    return dict(_REGISTRY)

def describe_tools():
    """Return a "name: description" list for the system prompt."""
    lines = []
    for name, fn in _REGISTRY.items():
        doc = (fn.__doc__ or "").strip().splitlines()
        desc = doc[0].strip() if doc else "(no description)"
        lines.append(f"- {name}: {desc}")
    return "\n".join(lines)
