import pytest
from lamine.types import Model


def test_valid_provider_no_locations():
    model = Model(provider="anthropic", id="claude-3.5-sonnet-latest")
    assert model.provider == "anthropic"
    assert model.locations is None


def test_valid_provider_with_supported_locations():
    model = Model(provider="vertex", id="gemini-1.5-flash-002", locations=["us-central1"])
    assert model.provider == "vertex"
    assert model.locations == ["us-central1"]


def test_valid_provider_with_multiple_supported_locations():
    model = Model(provider="vertex", id="gemini-1.5-flash-002", locations=["us-central1", "eu-central1"])
    assert model.provider == "vertex"
    assert model.locations == ["us-central1", "eu-central1"]


def test_invalid_location_for_provider():
    model = Model(provider="anthropic", id="claude-3.5-sonnet-latest", locations=["us-central1"])
    assert model
    # assert "Provider anthropic does not support `locations`." in caplog.text


def test_unsupported_provider():
    with pytest.raises(ValueError) as excinfo:
        Model(provider="unsupported-provider", id="model-id")
    assert str(excinfo.value).startswith("Provider unsupported-provider is not supported:")


def test_invalid_location_for_vertex_provider():
    model = Model(provider="vertex", id="gemini-2-flash", locations=["invalid-location"])
    assert model
    # assert "Provider vertex does not support location invalid-location:" in caplog.text


def test_valid_model_id_for_vertex_provider():
    model = Model(provider="vertex", id="gemini-1.5-pro-002")
    assert model.provider == "vertex"
    assert model.id == "gemini-1.5-pro-002"


def test_invalid_model_id_for_vertex_provider():
    model = Model(provider="vertex", id="invalid-model-id")
    assert model
    # assert "Provider vertex does not support model invalid-model-id:" in caplog.text
