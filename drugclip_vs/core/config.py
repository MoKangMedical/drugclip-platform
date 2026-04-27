"""
Screening configuration and constants.
"""

from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
import os


@dataclass
class ScreeningConfig:
    """Configuration for virtual screening pipeline."""
    
    # Model settings
    model_name: str = "drugclip"
    model_path: Optional[str] = None
    device: str = "auto"  # auto, cpu, mps, cuda
    
    # Stage 1: Fingerprint pre-screening
    fp_bits: int = 2048
    fp_radius: int = 2
    stage1_top_percent: float = 0.10  # Keep top 10%
    stage1_threshold: float = 0.0    # Minimum Tanimoto similarity
    
    # Stage 2: DrugCLIP re-ranking
    batch_size: int = 128
    max_candidates: int = 50000       # Max molecules for Stage 2
    
    # Output settings
    top_k: int = 100                  # Top-K results to return
    output_format: str = "csv"        # csv, json, sdf
    
    # Performance
    num_workers: int = 0              # 0 = auto-detect
    use_fp16: bool = True             # Half-precision inference
    
    # Paths
    cache_dir: str = ""
    
    def __post_init__(self):
        if not self.cache_dir:
            self.cache_dir = os.path.join(
                os.path.expanduser("~"), ".drugclip", "cache"
            )
        if self.device == "auto":
            import torch
            if torch.cuda.is_available():
                self.device = "cuda"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        if self.num_workers == 0:
            self.num_workers = max(1, os.cpu_count() // 2)


# Constants
DUD_E_TARGETS = [
    "aa2ar", "aces", "ada", "ada17", "adrb1", "adrb2", "akt1", "akt2",
    "aldr", "ampc", "andr", "aofb", "braf", "casp3", "cdk2", "comt",
    "cp2c9", "cp3a4", "cxcr4", "def", "dhi1", "dkk1", "dpp4", "drd3",
    "dyr", "egfr", "erbb2", "esr1", "esr2", "fa10", "fa7", "fak1",
    "fgfr1", "fkb1a", "fnta", "fpps", "gcr", "glcm", "gria2", "grik1",
    "hdac8", "hivint", "hivpr", "hivrt", "hmdh", "hs90a", "hxk4",
    "igf1r", "inha", "ital", "jak2", "kith", "kit", "kpcb", "lck",
    "lkha4", "mapk2", "mcr", "met", "mk01", "mk14", "mk10", "mmp13",
    "mp2k1", "nos1", "nram", "p85a", "parp1", "pde5a", "pgh1", "pgh2",
    "plk1", "pnph", "ppara", "pparg", "prgr", "ptn1", "pur2", "pygm",
    "pyrd", "reni", "rock1", "rxra", "sahh", "src", "tgfr1", "thb",
    "thrb", "try1", "tryb1", "tysy", "urok", "vgfr2", "wee1", "xiap"
]

LITPCBA_TARGETS = [
    "ADRB2", "ALDH1", "ESR1_ago", "ESR1_ant", "FEN1", "GBA",
    "IDH1", "KAT2A", "MAPK1", "MTORC1", "OPRK1", "PKM2",
    "PPARG", "TP53", "VDR"
]

ALL_TARGETS = DUD_E_TARGETS + LITPCBA_TARGETS
