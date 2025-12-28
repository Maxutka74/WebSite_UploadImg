import os
import sys
import signal
import subprocess
import time
import psutil
from watchfiles import watch, Change

from settings.logging_config import get_logger

logger = get_logger(__name__)

BASE_DIR = os.path.dirname(__file__)
APP_IMPORT = "app:app"
WATCH_DIRS = [BASE_DIR]


def kill_child_processes(parent_pid: int):
    try:
        parent = psutil.Process(parent_pid)
        children = parent.children(recursive=True)

        for child in children:
            child.terminate()

        _, alive = psutil.wait_procs(children, timeout=3)

        for child in alive:
            child.kill()

    except psutil.NoSuchProcess:
        logger.warning(f"Process {parent_pid} not found")


def terminate_process(process: subprocess.Popen | None, exit_code: int | None = None):
    if not process:
        return

    logger.info("Stopping server process...")
    kill_child_processes(process.pid)
    process.terminate()

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        logger.warning("Force killing server process")
        process.kill()

    if exit_code is not None:
        sys.exit(exit_code)


def run_server() -> subprocess.Popen:
    logger.info("Starting FastAPI server...")

    try:
        return subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                APP_IMPORT,
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


def main():
    logger.info("Development server with hot reload started")

    process = run_server()

    def signal_handler(sig, frame):
        logger.info("Shutdown signal received")
        terminate_process(process, exit_code=0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        def watch_filter(change: Change, path: str) -> bool:
            return path.endswith(".py")

        for changes in watch(*WATCH_DIRS, watch_filter=watch_filter):
            files = {os.path.basename(p) for _, p in changes}
            logger.info(f"Changes detected: {', '.join(files)}")
            logger.info("Restarting server...")

            terminate_process(process)
            time.sleep(1)

            process = run_server()
            logger.info("Server restarted")

    except KeyboardInterrupt:
        terminate_process(process, exit_code=0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        terminate_process(process, exit_code=1)


if __name__ == "__main__":
    main()
