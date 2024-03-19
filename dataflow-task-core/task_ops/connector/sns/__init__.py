import boto3

from task_ops.base import logutils
from task_ops.connector import Connector, ConnectorExitState

log = logutils.get_logger(__name__)


class SNSConnector(Connector):
    def __init__(self, name: str, subject: str, message: str):
        super().__init__(name)
        self.topic_arn = self.settings.get("topic_arn")
        self.subject = subject[:100]  # SNS limit
        self.message = message
        #  How to create SNSConnector for specific case ?  as below
        #  sns = SNSConnector("sns.terminate_ec2_instance", subject, message)

    def run(self) -> ConnectorExitState:
        sns = boto3.client('sns')
        response = sns.publish(TopicArn=self.topic_arn, Message=self.message, Subject=self.subject)
        log.debug(f"SNS: {response}")
        return ConnectorExitState.SUCCESS
