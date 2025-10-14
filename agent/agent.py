import os
import sys
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    RoomOutputOptions,
    WorkerOptions,
    cli,
    stt,
)
from livekit.plugins import silero, aws, azure, google
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variable STT_PROVIDER to select the STT provider
stt_provider = os.getenv("STT_PROVIDER", "").lower()


class Transcriber(Agent):
    def __init__(self, stt: stt.STT):
        super().__init__(
            instructions="not-needed",
            stt=stt,
        )


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


def get_stt_provider() -> stt.STT:
    if stt_provider == "aws":
        AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
        if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_DEFAULT_REGION:
            print(
                "AWS credentials or region not set. Please set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_DEFAULT_REGION environment variables."
            )
            sys.exit(1)
        return aws.STT(
            region=os.getenv("AWS_REGION"),
            access_key=os.getenv("AWS_ACCESS_KEY_ID"),
            secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
    elif stt_provider == "azure":
        AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
        AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
        AZURE_SPEECH_HOST = os.getenv("AZURE_SPEECH_HOST")
        if not AZURE_SPEECH_KEY or not AZURE_SPEECH_REGION or not AZURE_SPEECH_HOST:
            print(
                "Azure credentials or region not set. Please set AZURE_SPEECH_KEY, AZURE_SPEECH_REGION, and AZURE_SPEECH_HOST environment variables."
            )
            sys.exit(1)
        return azure.STT(
            region=os.getenv("AZURE_REGION"),
            subscription_key=os.getenv("AZURE_SUBSCRIPTION_KEY"),
        )
    elif stt_provider == "google":
        GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not GOOGLE_APPLICATION_CREDENTIALS:
            print(
                "Google credentials not set. Please set GOOGLE_APPLICATION_CREDENTIALS environment variable."
            )
            sys.exit(1)
        return google.STT(
            credentials_file=GOOGLE_APPLICATION_CREDENTIALS,
        )
    else:
        # If not declared or unsupported, print error and exit
        print(f"Unsupported or missing STT provider: {stt_provider}")
        print(
            "Declare environment variable STT_PROVIDER with one of the following values: [aws, azure, google]"
        )
        sys.exit(1)


async def entrypoint(ctx: JobContext):
    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        turn_detection=MultilingualModel(),
    )

    stt_instance = get_stt_provider()

    await session.start(
        agent=Transcriber(stt=stt_instance),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # The agent will only receive audio tracks as input
            text_enabled=False,
            video_enabled=False,
            audio_enabled=True,
            pre_connect_audio=True,
            pre_connect_audio_timeout=3.0,
        ),
        room_output_options=RoomOutputOptions(
            # The agent will only generate text transcriptions as output
            transcription_enabled=True,
            audio_enabled=False,
            sync_transcription=False,
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
