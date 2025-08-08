import yaml
import sys

def validate_render_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            print("YAML syntax is valid")
            print("\nConfiguration overview:")
            print("----------------------")
            if 'services' in config:
                for service in config['services']:
                    print(f"\nService: {service.get('name', 'unnamed')}")
                    print(f"Type: {service.get('type', 'not specified')}")
                    if 'env' in service:
                        print("Environment variables defined: Yes")
                    if 'buildCommand' in service:
                        print(f"Build command: {service['buildCommand']}")
                    if 'startCommand' in service:
                        print(f"Start command: {service['startCommand']}")
            return True
    except yaml.YAMLError as e:
        print(f"Error in configuration file: {e}")
        return False
    except FileNotFoundError:
        print(f"Could not find file: {file_path}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    config_file = "render.yaml"
    validate_render_config(config_file)
