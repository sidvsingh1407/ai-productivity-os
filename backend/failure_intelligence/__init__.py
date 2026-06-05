"""
Failure Intelligence Framework for TarkaX.
Provides APIs for analyzing assessment signals and identifying organizational failure patterns.
"""
from failure_intelligence.detection_engine import detect_failure_patterns
from failure_intelligence.pattern_library import FAILURE_PATTERNS

__all__ = ["detect_failure_patterns", "FAILURE_PATTERNS"]
