#!/usr/bin/env python3
"""Nexus - Advanced AI Aim-Assist System Entry Point (Production Ready)"""

import sys
import logging
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from nexus.utils.logger import setup_logger
from nexus.utils.config_manager import ConfigManager
from nexus.aim_assistant import AimAssistant

# Setup logging
logger = setup_logger(__name__, log_level="INFO")


def print_banner():
    """Print Nexus banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║              NEXUS - Advanced AI Aim-Assist               ║
    ║                                                            ║
    ║   Multi-Game Support | Physics Engine | Memory Access    ║
    ║   Ensemble Detection | Behavioral AI | Real-time 144fps  ║
    ║                                                            ║
    ║                        v1.0.0                             ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point"""
    print_banner()

    try:
        # Load configuration
        logger.info("Loading configuration...")
        config = ConfigManager.load("config.yaml")

        if not config:
            logger.error("Failed to load configuration")
            logger.error("Make sure config.yaml exists in the project root")
            return 1

        logger.info(f"Loaded game: {config.get('game', {}).get('name', 'Unknown')}")

        # Initialize aim-assist
        logger.info("Initializing Nexus system...")
        assistant = AimAssistant(config)

        # Start
        logger.info("Starting Nexus...")
        assistant.start()

        # Keep running
        try:
            while assistant.is_running:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")

        logger.info("Nexus shut down cleanly")
        return 0

    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.error("Run: pip install -r requirements.txt")
        return 1
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error("Make sure you're in the correct directory")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
