"""Configuración de pytest: agrega el layout src/ al path."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))