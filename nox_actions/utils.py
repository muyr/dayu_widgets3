# Import built-in modules
import os
import sys
from pathlib import Path

PACKAGE_NAME = "dayu_widgets3"
THIS_ROOT = Path(__file__).parent.parent
PROJECT_ROOT = THIS_ROOT.parent


def get_qt_dependencies(qt_binding: str) -> list[str]:
    """Get Qt dependencies based on binding type.
    
    Args:
        qt_binding: Either 'pyside2' or 'pyside6'
        
    Returns:
        List of package requirements
    """
    base_deps = [
        "pytest>=7.0.0",
        "pytest-qt>=4.2.0",
        "pytest-cov>=4.1.0",
        "qtpy>=2.4.0",
        "six>=1.16.0"  # 添加six作为依赖
    ]
    
    if qt_binding == "pyside2":
        return base_deps + ["PySide2==5.15.2.1"]
    return base_deps + ["PySide6==6.5.2"]


def setup_qt_test_env():
    """Setup environment for Qt testing.
    
    This ensures:
    1. The package is importable
    2. Qt can find necessary plugins
    """
    if THIS_ROOT not in sys.path:
        sys.path.insert(0, str(THIS_ROOT))
    
    # Set QT_QPA_PLATFORM for headless testing if needed
    if os.environ.get("CI") or os.environ.get("HEADLESS"):
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
