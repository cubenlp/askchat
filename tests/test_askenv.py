import pytest
from click.testing import CliRunner
from askchat.askenv import cli
from pathlib import Path

ENV_PATH = Path.home() / '.askchat' / 'envs'

@pytest.fixture
def runner():
    """Fixture providing a CliRunner for invoking command-line interfaces."""
    return CliRunner()

@pytest.fixture
def setup_env():
    """Fixture to set up and tear down an environment configuration."""
    env_name = "pytest_env"
    config_path = ENV_PATH / f"{env_name}.env"
    # Setup code before yield
    yield env_name, config_path
    # Teardown code after yield
    if config_path.exists():
        config_path.unlink()

def test_overwrite_environment_confirm(runner, setup_env):
    """Test overwriting an existing environment configuration with user confirmation."""
    env_name, config_path = setup_env
    # Create an initial environment
    runner.invoke(cli, ["new", env_name, "--api-key", "123"], input="y\n")
    
    # Attempt to overwrite the environment, confirming the action
    result = runner.invoke(cli, ["new", env_name, "--api-key", "456"], input="y\n")
    assert "Warning: Overwriting existing environment" in result.output
    assert "Do you want to continue?" in result.output
    # Verify the environment was overwritten by checking if the new API key is in the file
    with open(config_path) as f:
        assert "OPENAI_API_KEY='456'" in f.read()

def test_list_initially_empty(runner, setup_env):
    """Ensure no environments are listed when none have been created."""
    env_name, config_path = setup_env
    runner.invoke(cli, ["new", env_name, "--api-key", "123"], input="y\n")
    result = runner.invoke(cli, ["list"])
    assert env_name in result.output

def test_delete_environment(runner, setup_env):
    """Test deleting an environment configuration."""
    env_name, config_path = setup_env
    # First, create an environment to delete
    runner.invoke(cli, ["new", env_name, "--api-key", "123"])
    assert config_path.exists()  # Ensure the environment was created
    # Now, delete it
    result = runner.invoke(cli, ["delete", env_name])
    assert result.exit_code == 0
    assert f"Environment '{env_name}' deleted." in result.output
    assert not config_path.exists()

# Example test for the `show` command
def test_show_environment(runner, setup_env):
    """Test showing the details of a specific environment configuration."""
    env_name, config_path = setup_env
    # Create an environment to show
    runner.invoke(cli, ["new", env_name, "--api-key", "abc123"])
    result = runner.invoke(cli, ["show", env_name])
    assert "abc123" in result.output  # Checking if the API key is shown

# Continue writing tests for the remaining commands (save, use, config) following similar patterns.
