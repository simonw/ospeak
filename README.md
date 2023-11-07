# ospeak

[![PyPI](https://img.shields.io/pypi/v/ospeak.svg)](https://pypi.org/project/ospeak/)
[![Changelog](https://img.shields.io/github/v/release/simonw/ospeak?include_prereleases&label=changelog)](https://github.com/simonw/ospeak/releases)
[![Tests](https://github.com/simonw/ospeak/workflows/Test/badge.svg)](https://github.com/simonw/ospeak/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/ospeak/blob/master/LICENSE)

CLI tool for running text through the [OpenAI Text to speech](https://platform.openai.com/docs/guides/text-to-speech) API and speaking or saving the result

## Installation

Install this tool using `pipx`:

    pipx install ospeak

## Usage

To get your computer to say something, run:

    ospeak "Hello there"

You will need an OpenAI API key. You can set that as an environment variable:

    export OPENAI_API_KEY='...'

Or you can pass it using `--token`:

    ospeak --token '...' "Hello there"

You can pipe content into the tool:

    echo "Hello there" | ospeak

Use `-v/--voice VOICE` to select a voice. The default is `alloy`. The other options are:

- `echo`
- `fable`
- `onyx`
- `nova`
- `shimmer`

You can pass `-v all` to hear all of the voices, each with the name of the voice spoken first.

    ospeak 'This is my voice' -v all

To write the audio to a file, pass `-o/--output` with a filename ending in either `.mp3` or `.wav`:

    ospeak 'This is my voice' -o voice.mp3

This will not speak out loud. If you want it to also speak, add the `-s/--speak` option:

    ospeak 'This is my voice' -o voice.mp3 -s

## ospeak --help

<!-- [[[cog
import cog
from ospeak import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: ospeak")
cog.out(
    "```\n{}\n```".format(help)
)
]]] -->
```
Usage: ospeak [OPTIONS] [TEXT]

  CLI tool for running text through OpenAI Text to speech

Options:
  --version                       Show the version and exit.
  -v, --voice [alloy|echo|fable|onyx|nova|shimmer|all]
                                  Voice to use
  -o, --output FILE               Save audio to this file on disk
  -s, --speak                     Speak the text even when saving to a file
  --token TEXT                    OpenAI API key
  --help                          Show this message and exit.

```
<!-- [[[end]]] -->

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd ospeak
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
