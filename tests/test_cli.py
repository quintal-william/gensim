from typer.testing import CliRunner

from nsim import SUCCESS, __app_name__, __version__, cli


runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == SUCCESS
    assert f"{__app_name__} v{__version__}\n" in result.stdout

def test_version_short():
    result = runner.invoke(cli.app, ["-v"])
    assert result.exit_code == SUCCESS
    assert f"{__app_name__} v{__version__}\n" in result.stdout
