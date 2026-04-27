"""
DrugClip Virtual Screening Platform
====================================
AI-powered virtual screening for drug discovery using DrugCLIP contrastive learning.
"""

__version__ = "1.0.0"
__author__ = "MoKangMedical"

from drugclip_vs.core.screener import VirtualScreener
from drugclip_vs.core.config import ScreeningConfig

__all__ = ["VirtualScreener", "ScreeningConfig"]
