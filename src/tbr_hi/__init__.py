"""Target-conditioned Behavior–Relevance Harsanyi Interaction (TBR-HI)."""

from .decomposition import decompose_loss_tables
from .players import BRTPlayer, covered_players, group_players

__version__ = '0.1.0'
__all__ = ['BRTPlayer', 'covered_players', 'group_players', 'decompose_loss_tables']
