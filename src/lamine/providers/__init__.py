import os

dir = os.path.dirname(os.path.abspath(__file__))
PROVIDER_IDS = list()
for script in os.listdir(dir):
    file_name, extension = os.path.splitext(script)
    if not file_name.startswith("_") and extension == ".py":
        PROVIDER_IDS.append(file_name)
