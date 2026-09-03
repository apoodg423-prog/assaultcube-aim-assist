"""Configuration Manager"""

import logging
import yaml
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigManager:
    """Load and manage configuration"""

    @staticmethod
    def load(config_path: str) -> Dict[str, Any]:
        """Load YAML configuration"""
        try:
            config_file = Path(config_path)
            if not config_file.exists():
                logger.error(f"Config file not found: {config_path}")
                return {}

            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"Loaded config from {config_path}")
                return config or {}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}

    @staticmethod
    def save(config: Dict[str, Any], config_path: str):
        """Save configuration to YAML"""
        try:
            config_file = Path(config_path)
            config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
                logger.info(f"Saved config to {config_path}")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
