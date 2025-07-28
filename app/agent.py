from typing import AsyncGenerator, Dict, Any, Union
from pydantic import BaseModel, Field
from claude_code_sdk import (
    ClaudeCodeOptions,
    ToolUseBlock,
    TextBlock,
    query,
    AssistantMessage,
    ResultMessage,
)


class StreamingToolUse(BaseModel):
    type: str = Field(default="tool_use")
    name: str
    input: Dict[str, Any]


class StreamingTextBlock(BaseModel):
    type: str = Field(default="text")
    text: str


class StreamingResultMessage(BaseModel):
    type: str = Field(default="result")
    is_error: bool
    result: str | None


async def run(
    question: str,
) -> AsyncGenerator[
    Union[StreamingToolUse, StreamingTextBlock, StreamingResultMessage],
    None,
]:
    system_prompt = """
        You are a helpful assistant who triages Jira tickets.

        When provided with a description of a Jira escalation, determine if:
        1. This is a supported feature in the system
        2. If this is a bug - if it is, where the bug is located

        Your response should include rationale for whether or not the workflow
        described in the ticket is actually supported and this is a true bug.
    """

    options = ClaudeCodeOptions(
        cwd="/app/btiq",
        max_turns=100,
        allowed_tools=[
            "Task",
            "Bash",
            "Glob",
            "Grep",
            "LS",
            "ExitPlanMode",
            "Read",
            "NotebookRead",
            "NotebookEdit",
            "WebFetch",
            "TodoWrite",
            "WebSearch",
        ],
        disallowed_tools=["Write", "Edit", "MultiEdit"],
        system_prompt=system_prompt,
        model="",
    )

    async for message in query(prompt=question, options=options):
        try:
            if isinstance(message, AssistantMessage):
                if hasattr(message, "content"):
                    # Check for TextBlock first
                    text_block = next(
                        (
                            item
                            for item in message.content
                            if isinstance(item, TextBlock)
                        ),
                        None,
                    )

                    if text_block is not None:
                        yield StreamingTextBlock(text=text_block.text)

                    # Check for ToolUseBlock
                    tool_use_block = next(
                        (
                            item
                            for item in message.content
                            if isinstance(item, ToolUseBlock)
                        ),
                        None,
                    )

                    if tool_use_block is not None:
                        yield StreamingToolUse(
                            name=tool_use_block.name, input=tool_use_block.input
                        )
            elif isinstance(message, ResultMessage):
                yield StreamingResultMessage(
                    is_error=message.is_error, result=message.result
                )
        except Exception as e:
            print(f"Exception: ${e}")
