import yaml

def read_yaml_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_yaml_file(file_path: str, content: dict):
    with open(file_path, 'w') as file:
        yaml.dump(content, file)