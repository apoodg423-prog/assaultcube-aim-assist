# Packaging notes for Windows

This folder outlines steps to package Ipro71 Nexus for Windows using PyInstaller.

1. Create a virtualenv and install requirements (prefer CPU-only torch if packaging without CUDA):
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt

2. Build:
   pyinstaller --onefile --noconsole app/run.py --add-data "nexus;./nexus" --name "Ipro71 Nexus"

3. Code signing and MSI creation are outside the scope here. Use WiX Toolset or Inno Setup for installer creation.
