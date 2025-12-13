from pathlib import Path

import yaml

from main import app


def generate_openapi():
    openapi_schema = app.openapi()
    
    yaml_path = Path("openapi.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(openapi_schema, f, default_flow_style=False, 
                  allow_unicode=True, sort_keys=False)
    print(f"✅ Generated {yaml_path}")

if __name__ == "__main__":
    generate_openapi()