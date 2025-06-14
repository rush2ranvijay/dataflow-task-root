from sqlalchemy import create_engine
from sqlalchemy.sql import text
import datetime

from task_ops.base import logutils

log = logutils.get_logger(__name__)


class TaskStatus:
    """Helper class to help manage Task's status in the SCDF DB."""

    def __init__(self, task_id, jdbc_url):
        self.task_id = task_id
        self.engine = create_engine(jdbc_url)

    def running(self):
        """Set the TASK_EXECUTION's START_TIME."""
        now = datetime.datetime.now()
        start_task_statement = text(
            "UPDATE TASK_EXECUTION SET START_TIME=:start_time, EXIT_CODE=null, LAST_UPDATED=:last_updated "
            "WHERE TASK_EXECUTION_ID=:task_id"
        )
        with self.engine.begin() as conn:
            conn.execute(start_task_statement, {
                "start_time": now,
                "last_updated": now,
                "task_id": self.task_id
            })
        log.debug(f"Task Execution Status Changed to Running for TASK_EXECUTION_ID: {self.task_id}")

    def completed(self):
        """Set the TASK_EXECUTION's END_TIME, EXIT_CODE=0, and EXIST_MESSAGE/ERROR_MESSAGE must be null."""
        now = datetime.datetime.now()
        complete_task_statement = text(
            "UPDATE TASK_EXECUTION SET END_TIME=:end_time, EXIT_CODE=0, EXIT_MESSAGE=null, ERROR_MESSAGE=null, "
            "LAST_UPDATED=:last_updated WHERE TASK_EXECUTION_ID=:task_id"
        )
        with self.engine.begin() as conn:
            conn.execute(complete_task_statement, {
                "end_time": now,
                "last_updated": now,
                "task_id": self.task_id
            })
        log.debug(f"Task Execution Completed for TASK_EXECUTION_ID: {self.task_id}")

    def failed(self, exit_code, exit_message, error_message=''):
        """Set the TASK_EXECUTION's END_TIME, EXIT_CODE is the error code and EXIT_MESSAGE/ERROR_MESSAGE describe
        the error."""
        now = datetime.datetime.now()
        complete_task_statement = text(
            "UPDATE TASK_EXECUTION SET END_TIME=:end_time, EXIT_CODE=:exit_code, EXIT_MESSAGE=:exit_message, "
            "ERROR_MESSAGE=:error_message, LAST_UPDATED=:last_updated WHERE TASK_EXECUTION_ID=:task_id"
        )
        with self.engine.begin() as conn:
            conn.execute(complete_task_statement, {
                "end_time": now,
                "exit_code": exit_code,
                "exit_message": exit_message,
                "error_message": error_message,
                "last_updated": now,
                "task_id": self.task_id
            })
        log.debug(f"Task Execution Failed for TASK_EXECUTION_ID: {self.task_id}")

