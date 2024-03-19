import abc
import enum
from abc import abstractmethod
from typing import Any

from task_ops.base import logutils
from task_ops.base.environments import Environment
from task_ops.task_base.task_status import TaskStatus

log = logutils.get_logger(__name__)


class TaskRunStatus(enum.Enum):
    """
    Generic exit status return by connector to indicate the success or failure state
    """
    SUCCESS = 0
    TIMEOUT = 5
    ERROR = 6


def load_task_settings(env: Environment, dataflow_task_name: str) -> dict:
    """
        This method loads all the configuration of the Job, base on its name given in defaults.yaml
    """
    return env.get_section(dataflow_task_name)


class BaseTask(abc.ABC):
    """
        BaseTask class which has been extended by all the python tasks classes
    """

    def __init__(self, dataflow_task_name: str, env: Environment, **kwargs):
        self.dataflow_task_name = dataflow_task_name
        self.env = env
        self.settings = load_task_settings(env, dataflow_task_name)
        self.validations = list()

    def get_setting(self, key: str, fallback: Any) -> Any:
        return self.settings.get(key, fallback)

    def parse_inputs(self):
        pass

    def run(self, **kwargs) -> TaskRunStatus:
        """
            BaseTask class template method needs to override by its child class .
        """
        step = None
        try:
            log.debug(f"Running Task [ {self.dataflow_task_name} ] with args: {kwargs}")
            step = "PRE_RUN"
            self.pre_run(**kwargs)
            step = "RUN"
            run_status = self.do_run(**kwargs)
            log.debug(f"Executed Task [ {self.dataflow_task_name} ] and post_run life-cycle method is started")
            step = "POST_RUN"
            self.post_run(**kwargs)
        except TimeoutError as e:  # flake8: noqa
            log.exception(f"Timeout error occurred: {e}")
            raise
        except Exception as e:  # flake8: noqa
            log.exception(f"Unhandled exception occurred in step '{step}' for Task '{self.dataflow_task_name}': {e}")
            raise
        finally:
            self.write_validations()
        return run_status

    @abstractmethod
    def do_run(self, **kwargs):
        pass

    def pre_run(self, **kwargs):
        pass

    def post_run(self, **kwargs):
        pass

    def write_validations(self):
        # simplest implementation of logging validations
        log.info(f"{self.validations}")


class DataFlowBaseTask(BaseTask):
    """
    DataFlowBaseTask class which extends BaseTask to manage task status in SCDF database.
    """

    def __init__(self, dataflow_task_name: str, env: Environment, **kwargs):
        super().__init__(dataflow_task_name, env, **kwargs)
        self.task_id = None
        self.jdbc_url = None
        self.task_status = None
        self.init_task_status(**kwargs)

    def init_task_status(self, **kwargs):
        # Initialize TaskStatus with task_id and jdbc_url
        self.task_id = kwargs.get("task_id")
        self.jdbc_url = kwargs.get("jdbc_url")
        if self.task_id and self.jdbc_url:
            self.task_status = TaskStatus(task_id=self.task_id, jdbc_url=self.jdbc_url)

    def do_run(self, **kwargs) -> TaskRunStatus:
        """
        Override do_run method to run the task and update status.
        """
        try:
            if self.task_status:
                self.task_status.running()  # Mark task as running
            self.execute_dataflow_task(**kwargs)   # Running Actual task workload
            if self.task_status:
                self.task_status.completed()  # Mark task as completed
            self.on_success(**kwargs)
            return TaskRunStatus.SUCCESS
        except Exception as e:
            if self.task_status:
                self.task_status.failed(exit_code=1, exit_message="Task failed", error_message=str(e))
            self.on_failure(e, **kwargs)
            return TaskRunStatus.ERROR

    @abstractmethod
    def execute_dataflow_task(self, **kwargs):
        """ Abstract method to be implemented by subclasses for executing the dataflow task. """
        pass

    def on_success(self, **kwargs):
        pass

    def on_failure(self, e: Exception, **kwargs):
        pass
