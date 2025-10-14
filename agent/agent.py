"""Simple LiveKit transcription agent using AWS Transcribe."""

import os
from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    WorkerType,
    cli,
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
    await session.start(agent=agent, room=ctx.room)

    # Connect to room and subscribe to audio only
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)


# Configure worker type from environment variable
worker_type = os.getenv("AGENT_WORKER_TYPE", "room")
worker_type = WorkerType[worker_type.upper()]

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint, prewarm_fnc=prewarm, worker_type=worker_type
        )
    )
