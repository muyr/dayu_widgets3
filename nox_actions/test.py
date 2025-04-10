# Import built-in modules
from pathlib import Path
from typing import Optional

# Import third-party modules
import nox
from nox_actions.utils import get_qt_dependencies


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"])
@nox.parametrize("qt_binding", ["pyside2", "pyside6"])
def test(session: nox.Session, qt_binding: str, dcc: Optional[str] = None) -> None:
    """Run tests with specific Qt binding and Python version.

    Args:
        session: The nox session
        qt_binding: Qt binding to use ('pyside2' or 'pyside6')
        dcc: DCC environment to simulate ('maya', 'blender', or None for standalone)
    """
    # Get the project root directory
    root_dir = Path(__file__).parent.parent.absolute()

    # 检查Python版本和Qt绑定的兼容性
    import sys
    if qt_binding == "pyside2" and sys.version_info >= (3, 11):
        session.skip("PySide2 is not supported on Python 3.11+")
        return

    # Install dependencies first
    deps = get_qt_dependencies(qt_binding)
    if not deps:  # 如果依赖列表为空，说明需要跳过测试
        session.skip("No dependencies available for this configuration")
        return

    for dep in deps:
        session.install(dep)

    # Then install the package itself
    if qt_binding == "pyside2":
        session.install("-e", ".[pyside2]")
    else:
        session.install("-e", ".[pyside6]")

    # Set environment variables
    env = {
        "QT_API": qt_binding,
        "PYTHONPATH": str(root_dir)
    }

    # Set DCC environment variable if specified
    if dcc:
        env["DAYU_TEST_DCC"] = dcc.upper()
        session.log(f"Running tests in simulated {dcc.upper()} environment")
    else:
        session.log("Running tests in standalone environment")

    # Run tests
    session.run(
        "pytest",
        "tests",
        "-v",
        "--cov=dayu_widgets",
        "--cov-report=xml",
        "--cov-report=term",
        "--cov-report=html",
        "--cov-fail-under=70",
        env=env
    )


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"])
@nox.parametrize("qt_binding", ["pyside2", "pyside6"])
def test_maya(session: nox.Session, qt_binding: str) -> None:
    """Run tests in Maya environment.

    Args:
        session: The nox session
        qt_binding: Qt binding to use ('pyside2' or 'pyside6')
    """
    # Skip PySide2 tests on Python 3.11+
    import sys
    if qt_binding == "pyside2" and sys.version_info >= (3, 11):
        session.skip("PySide2 is not supported on Python 3.11+")
        return

    # Run tests in Maya environment
    test(session, qt_binding=qt_binding, dcc="maya")


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"])
@nox.parametrize("qt_binding", ["pyside2", "pyside6"])
def test_blender(session: nox.Session, qt_binding: str) -> None:
    """Run tests in Blender environment.

    Args:
        session: The nox session
        qt_binding: Qt binding to use ('pyside2' or 'pyside6')
    """
    # Skip PySide2 tests on Python 3.11+
    import sys
    if qt_binding == "pyside2" and sys.version_info >= (3, 11):
        session.skip("PySide2 is not supported on Python 3.11+")
        return

    # Run tests in Blender environment
    test(session, qt_binding=qt_binding, dcc="blender")
