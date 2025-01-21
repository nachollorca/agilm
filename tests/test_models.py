import os

import pytest

from lamine.datatypes import Model


def test_unsupported_provider():
    with pytest.raises(ValueError) as excinfo:
        Model(provider="unsupported-provider", id="model-id")
    assert str(excinfo.value).startswith("Provider 'unsupported-provider' is not supported:")


def test_false_env_vars():
    if os.getenv("var1"):
        del os.environ["var1"]
    with pytest.raises(EnvironmentError) as excinfo:
        Model("mock", "model1")
    assert str(excinfo.value) == "Provider 'mock' requires environmental variable 'var1'"


def test_correct_env_vars():
    os.environ["var1"] = "mock"
    model = Model("mock", "model1")
    assert model.provider == "mock"


def test_valid_model():
    model = Model(provider="mock", id="model1")
    assert model.provider == "mock"
    assert model.id == "model1"


def test_invalid_model():
    Model(provider="mock", id="invalid-model")
    # assert "Provider 'mock' does not support model 'invalid-model'"


def test_valid_locations():
    model = Model(provider="mock", id="model1", locations=["location1"])
    assert model.locations == ["location1"]


def test_invalid_locations():
    Model(provider="mock", id="invalid-model", locations=["location3"])
    # assert "Provider 'mock' does not support model 'location3'"
