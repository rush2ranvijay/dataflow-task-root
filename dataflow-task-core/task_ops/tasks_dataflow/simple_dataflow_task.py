from task_ops.base.environments import env
from task_ops.task_base import get_dataflow_task_section
from task_ops.task_base.base import DataFlowBaseTask


class SimpleDataflowTask(DataFlowBaseTask):
    def __init__(self, dataflow_task_name, config, **kwargs):
        super().__init__(dataflow_task_name, env, **kwargs)
        self.dataflow_task_name = dataflow_task_name
        self.dataflow_task_section = get_dataflow_task_section(self.dataflow_task_name, None)
        self.dataflow_task_config = get_dataflow_task_section(self.dataflow_task_name, config)

    def execute_dataflow_task(self, **kwargs):
        print(f"Simple Task [ {self.dataflow_task_name} ] has been Started with config [ {self.dataflow_task_section} ] ")


def main():
    return SimpleDataflowTask("simple_task", "config").run()


if __name__ == '__main__':
    main()
