#!/usr/bin/env python

"""Tests for `askchat` package."""

import pytest
from click.testing import CliRunner
from askchat import cli

# Fixture to initialize and tear down resources if needed
@pytest.fixture
def runner():
    return CliRunner()

def test_version_option(runner):
    """Test the --version option."""
    result = runner.invoke(cli.main, ['--version'])
    assert result.exit_code == 0
    assert "askchat version:" in result.output

def test_valid_models_option(runner):
    """Test the --valid-models option."""
    result = runner.invoke(cli.main, ['--valid-models'])
    assert result.exit_code == 0
    assert "Valid models that contain \"gpt\" in their names:" in result.output

def test_all_valid_models_option(runner):
    """Test the --all-valid-models option."""
    result = runner.invoke(cli.main, ['--all-valid-models'])
    assert result.exit_code == 0
    assert "All valid models:" in result.output

# Add more tests here based on the functionality you wish to test
