from pathlib import Path
import os
from ..utils import BaseEnum

dir = Path(__file__).parent.resolve()
provider_ids = [provider.split(".")[0] for provider in os.listdir(f"{dir}") if provider.endswith(".py")]
PROVIDERS = BaseEnum.from_list(name="providers", lst=provider_ids)
