import asyncio
from typing import TypedDict, Callable, Any

class FunctionCall(TypedDict):
    func: Callable[..., Any]
    args: list[Any]
    kwargs: dict[str, Any]

async def delay_execution(delay: float, *functions: FunctionCall) -> None:
    await asyncio.sleep(delay)

    for function in functions:
        result: Any = function['func'](*function['args'], **function['kwargs'])
        if asyncio.iscoroutine(result):
            await result