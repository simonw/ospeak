from click.testing import CliRunner
from ospeak.cli import cli
import pytest

runner = CliRunner()


def test_output_file_format():
    result = runner.invoke(cli, ["--output", "test.txt", "Hello"])
    assert result.exit_code == 2
    assert "Output file must be .mp3 or .wav format" in result.output


def test_voice_all_with_output():
    result = runner.invoke(cli, ["--voice", "all", "--output", "test.mp3", "Hello"])
    assert result.exit_code == 2
    assert "Cannot use --voice=all when saving to a file" in result.output


def test_speed_out_of_bounds():
    result = runner.invoke(cli, ["--speed", "5.0", "Hello"])
    assert result.exit_code == 2
    assert "Invalid value for " in result.output
    result2 = runner.invoke(cli, ["--speed", "0", "Hello"])
    assert result2.exit_code == 2
    assert "Invalid value for " in result2.output


@pytest.mark.parametrize("invalid_voice", ["unknown", "invalid", "123"])
def test_invalid_voice_option(invalid_voice):
    result = runner.invoke(cli, ["--voice", invalid_voice, "Hello"])
    assert result.exit_code == 2
    # You would replace this assert with a check for the actual error message you expect
    assert "Invalid value for " in result.output
