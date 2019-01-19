import os
import signal

from traceback import print_tb

from ._cfnresponse import SUCCESS, FAILED, send

## Trek10 local testing
if os.getenv('AWS_EXECUTION_ENV') is None:
    send = print

    class Context:
        @staticmethod
        def get_remaining_time_in_millis():
            return 3000


class CfnContext:
    """CloudFormation does not play nice if a CustomResource crashes without responding.
       This context manager tries to catch all possible failures and respond.
    """

    @staticmethod
    def __timeout(signum, frame):
        raise RuntimeError("NO REMAINING CONTEXT EXECUTION TIME")

    def __init__(self,
                 event,
                 context,
                 delete_immediate_success=True,
                 no_echo=False):
        (self.event, self.context, self.properties,
         self.no_echo) = (event, context, event.get('ResourceProperties', {}),
                          no_echo)
        self.logical_id = event.get('LogicalResourceId', '${AWS::StackName}')
        self.physical_id = event.get('PhysicalResourceId', self.logical_id)
        if delete_immediate_success and event.get(
                'RequestType', 'Delete').casefold() == 'delete':
            print(f"DELETE IMMEDIATE SUCCESS")
            self.success()

        signal.signal(signal.SIGALRM, self.__timeout)
        remaining_time = (context.get_remaining_time_in_millis() - 100) / 1000
        signal.setitimer(signal.ITIMER_REAL, remaining_time)

    def __enter__(self):
        return self

    def send(self,
             response=FAILED,
             resource_properties=None,
             physical_id=None,
             reason=None):
        self.properties = resource_properties if resource_properties is not None else self.properties
        self.physical_id = physical_id if resource_properties is not None else self.physical_id
        send(self.event, self.context, response, self.properties,
             self.physical_id, reason, self.no_echo)

    def failed(self, resource_properties=None, physical_id=None, reason=None):
        self.send(FAILED, resource_properties, physical_id, reason)

    def success(self, resource_properties=None, physical_id=None, reason=None):
        self.send(SUCCESS, resource_properties, physical_id, reason)

    def __exit__(self, type_, value, tb):
        signal.setitimer(signal.ITIMER_REAL, 0)
        if tb:
            reason = f"{type_.__name__}: {value}"
            print(reason)
            print_tb(tb)
            self.failed(reason=reason)
        else:
            self.success(reason='Custom resource successful!')
