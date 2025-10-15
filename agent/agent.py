"""Simple LiveKit transcription agent using AWS Transcribe."""

import os
import sys
from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    WorkerType,
    cli,
    RoomOutputOptions,
    RoomInputOptions,
)
from livekit.plugins import aws, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel


def prewarm(proc: JobProcess):
    """Preload the VAD model to speed up agent startup."""
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    """Main agent entry point - sets up transcription and connects to room."""
    # Configure AWS Transcribe STT (uses AWS env vars for credentials)
    stt = aws.STT(language="en-US")

    # Create a simple agent with STT
    agent = Agent(instructions="not-needed", stt=stt)

    # Create agent session with VAD and turn detection
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        turn_detection=MultilingualModel(),
    )

    # Start the session
    await session.start(
        agent=agent,
        room=ctx.room,
        room_output_options=RoomOutputOptions(
            # The agent will only generate text transcriptions as output
            transcription_enabled=True,
            audio_enabled=False,
        ),
        room_input_options=RoomInputOptions(
            # The agent will only receive audio tracks as input
            text_enabled=False,
            video_enabled=False,
            audio_enabled=True,
            pre_connect_audio=True,
            pre_connect_audio_timeout=3.0,
        ),
    )

    # Connect to room and subscribe to audio only
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)


# Apply log level from env var
log_level = os.getenv("LOG_LEVEL", "debug").upper()
sys.argv.append(f"--log-level={log_level}")
print(f"Applied log level {log_level}")

worker_options = WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm)

# Configure worker type from env var
worker_type = os.getenv("AGENT_WORKER_TYPE", "room")
worker_type = WorkerType[worker_type.upper()]
worker_options.worker_type = worker_type

# Optionally configure agent name from env var
agent_name = os.getenv("AGENT_NAME")
if agent_name:
    print(f"Starting agent prepared for manual dispatch with name: {agent_name}")
    worker_options.agent_name = agent_name
else:
    print("Starting agent prepared for automatic dispatch")

if __name__ == "__main__":
    cli.run_app(worker_options)
