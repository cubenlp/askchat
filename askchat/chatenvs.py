import click
from pathlib import Path
from . import write_config
from dotenv import set_key

# Main environment file
MAIN_ENV_PATH = Path.home() / '.askchat' / '.env'
# Env directory
ENV_PATH = Path.home() / '.askchat' / 'envs'

@click.group()
def cli():
    """askenvs CLI for managing askchat environments."""
    if not ENV_PATH.exists():
        ENV_PATH.mkdir(parents=True)

@cli.command()
def list():
    """List all environment configurations."""
    configs = [env for env in ENV_PATH.glob('*.env')]
    if configs:
        click.echo("Available environments:")
        for config in configs:
            click.echo(f"- {config.stem}")
    else:
        click.echo("No environments found in ~/.askchat/envs.")

@cli.command()
@click.argument('name')
@click.option('-a', '--api-key', default=None, help='API key')
@click.option('-b', '--base-url', default=None, help='Base URL of the API (without suffix `/v1`)')
@click.option('--api-base', default=None, help='Base URL of the API (with suffix `/v1`)')
@click.option('-m', '--model', default=None, help='Model name')
def create(name, api_key, base_url, api_base, model):
    """Create a new environment configuration."""
    config_path = ENV_PATH / f'{name}.env'
    if config_path.exists():
        click.echo(f"Environment '{name}' already exists." +\
                   "Use 'askenvs delete' to delete it first.")
    else:
        write_config(config_path, api_key, model, base_url, api_base)
        click.echo(f"Environment '{name}' created.")

@cli.command()
@click.argument('name', required=False)  # Make 'name' argument optional
@click.option('--default', is_flag=True, help='Delete the default environment configuration')
def delete(name, default):
    """Delete an environment configuration."""
    if default:
        default_config_path = MAIN_ENV_PATH
        if default_config_path.exists():
            default_config_path.unlink()
            click.echo("Default environment configuration deleted.")
        else:
            click.echo("No default environment configuration found.")
    else:
        if not name:
            click.echo("Please specify an environment name or use --default to delete the default configuration.")
            return
        config_path = ENV_PATH / f'{name}.env'
        if config_path.exists():
            config_path.unlink()
            click.echo(f"Environment '{name}' deleted.")
        else:
            click.echo(f"Environment '{name}' not found.")

@cli.command()
def current():
    """Print current environment variables."""
    if MAIN_ENV_PATH.exists():
        with MAIN_ENV_PATH.open() as f:
            click.echo(f.read())
    else:
        click.echo("No active environment." +\
                   "You can use `askchat --generate-config` to create one.")

@cli.command()
@click.argument('name')
def save(name):
    """Save the current environment variables to a file."""
    if MAIN_ENV_PATH.exists():
        content = MAIN_ENV_PATH.read_text()
        config_path = ENV_PATH / f'{name}.env'
        config_path.write_text(content)
        click.echo(f"Environment '{name}' saved.")
    else:
        click.echo("No active environment to save.")

@cli.command()
@click.argument('name')
def activate(name):
    """Activate an environment by replacing the .env file."""
    config_path = ENV_PATH / f'{name}.env'
    if config_path.exists():
        content = config_path.read_text()
        MAIN_ENV_PATH.write_text(content)
        click.echo(f"Environment '{name}' activated.")
    else:
        click.echo(f"Environment '{name}' not found.")

@cli.command()
@click.option('-a', '--api-key', help='API key')
@click.option('-b', '--base-url', help='Base URL of the API (without suffix `/v1`)')
@click.option('--api-base', help='Base URL of the API (with suffix `/v1`)')
@click.option('-m', '--model', help='Model name')
def env(api_key, base_url, api_base, model):
    """Update default .env values."""
    updated = False
    MAIN_ENV_PATH.touch(exist_ok=True)
    if api_key:
        set_key(MAIN_ENV_PATH, "API_KEY", api_key)
        updated = True
    if base_url:
        set_key(MAIN_ENV_PATH, "BASE_URL", base_url)
        updated = True
    if api_base:
        set_key(MAIN_ENV_PATH, "API_BASE", api_base)
        updated = True
    if model:
        set_key(MAIN_ENV_PATH, "MODEL", model)
        updated = True
    if updated:
        click.echo("Default environment updated.")
    else:
        click.echo("No updates made. Provide at least one option to update.")

if __name__ == '__main__':
    cli()
