import pytest
from agilm.types import Model

def test_valid_provider_no_locations():
    model = Model(provider="anthropic", id="model-id")
    assert model.provider == "anthropic"
    assert model.locations is None

def test_valid_provider_with_supported_locations():
    model = Model(provider="vertex", id="model-id", locations=["us-central1"])
    assert model.provider == "vertex"
    assert model.locations == ["us-central1"]

def test_valid_provider_with_multiple_supported_locations():
    model = Model(provider="vertex", id="model-id", locations=["us-central1", "eu-central1"])
    assert model.provider == "vertex"
    assert model.locations == ["us-central1", "eu-central1"]

def test_invalid_location_for_provider():
    with pytest.raises(ValueError) as excinfo:
        Model(provider="anthropic", id="model-id", locations=["us-central1"])
    assert str(excinfo.value) == "Provider anthropic does not support `locations`."

def test_unsupported_provider():
    with pytest.raises(ValueError) as excinfo:
        Model(provider="unsupported-provider", id="model-id")
    assert str(excinfo.value).startswith("Provider unsupported-provider is not supported:")

def test_invalid_location_for_vertex_provider():
    with pytest.raises(ValueError) as excinfo:
        Model(provider="vertex", id="model-id", locations=["invalid-location"])
    assert str(excinfo.value).startswith("Location invalid-location not supported for vertex:")