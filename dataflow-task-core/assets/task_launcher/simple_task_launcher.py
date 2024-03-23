import sys

from task_ops.base import logutils
from task_ops.tasks_dataflow.simple_dataflow_task import SimpleDataflowTask

log = logutils.get_logger(__name__)


def main():
    return SimpleDataflowTask("simple_task", "config", **{"sys_argv": sys.argv}).run()


if __name__ == "__main__":
    main()
