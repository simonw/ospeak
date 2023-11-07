import io
import sys

import click
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play

VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def stream_and_play(
    text, voice="alloy", speed=1.0, speak=True, api_key=None, output=None
):
    client = OpenAI(api_key=api_key)
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        speed=speed,
    )
    byte_stream = io.BytesIO(response.content)
    audio = AudioSegment.from_file(byte_stream, format="mp3")
    # Doesn't output ffmpeg info provided simpleaudio is installed:
    if speak:
        play(audio)
    if output:
        audio.export(output, format=output.rsplit(".", 1)[-1])


@click.command()
@click.version_option()
@click.argument("text", required=False)
@click.option(
    "-v",
    "--voice",
    help="Voice to use",
    type=click.Choice(VOICES + ["all"]),
)
@click.option(
    "-o",
    "--output",
    help="Save audio to this file on disk",
    # Must be writable file path
    type=click.Path(writable=True, dir_okay=False, resolve_path=True, allow_dash=False),
)
@click.option(
    "-x",
    "--speed",
    help="Speed of the voice",
    type=click.FloatRange(0.25, 4.0),
    default=1.0,
)
@click.option(
    "-s",
    "--speak",
    is_flag=True,
    help="Speak the text even when saving to a file",
)
@click.option(
    "--token",
    help="OpenAI API key",
    envvar="OPENAI_API_KEY",
)
def cli(text, voice, output, speed, speak, token):
    "CLI tool for running text through OpenAI Text to speech"
    if output:
        if not (output.endswith(".mp3") or output.endswith(".wav")):
            raise click.BadOptionUsage(
                "output", "Output file must be .mp3 or .wav format"
            )
    if not text:
        text = sys.stdin.read()
    if voice == "all":
        if output:
            raise click.BadOptionUsage(
                "voice", "Cannot use --voice=all when saving to a file"
            )
        for voice in VOICES:
            stream_and_play(voice.title() + ".\n\n" + text, voice, speed, True, token)
    else:
        if not voice:
            voice = VOICES[0]
        stream_and_play(text, voice, speed, speak or not output, token, output)
