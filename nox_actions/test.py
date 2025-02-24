# Import built-in modules
from pathlib import Path

# Import third-party modules
import nox
from nox_actions.utils import get_qt_dependencies

@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"])
@nox.parametrize("qt_binding", ["pyside2", "pyside6"])
def test(session: nox.Session, qt_binding: str) -> None:
    """Run tests with specific Qt binding and Python version."""
    # Get the project root directory
    root_dir = Path(__file__).parent.parent.absolute()
    
    # Install dependencies first
    for dep in get_qt_dependencies(qt_binding):
        session.install(dep)
    
    # Then install the package itself
    session.install("-e", ".")
    
    # Set environment variables
    env = {
        "QT_API": qt_binding,
        "PYTHONPATH": str(root_dir)
    }
    
    # Run tests
    session.run(
        "pytest",
        "tests",
        "-v",
        env=env
    )
