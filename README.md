# LBR Context Manager

The best tool for AWS lambda-backed custom resources since sliced cheese!

## How is it used

I'm glad you asked!

First `pip install lbr-context`, then in your custom resource handler:

```python
from lbr_context import CfnContext


def handler(event=None, context=None):
    event = event or {}
    request_type = event['RequestType'].upper()
    with CfnContext(event, context) as cfn:
        if 'CREATE' in request_type:
            # handle a create here
            pass
        elif 'UPDATE' in request_type:
            # handle an update here
            pass
        elif 'DELETE' in request_type:
            # handle a delete here
            pass
```

## So what makes this better

One of the big pains experienced when writing custom resources is getting it wrong, because this can cause your resource to be in an `IN_PROGRESS` state for a long time.

This context manager addresses that, and will catch any uncaught exception. When it catches an exception, it sends the `FAILED` request to the `event`'s endpoint, so CloudFormation knows your custom resource failed to create/update/delete.

On top of that, this context manager sets a timer for when the lambda is about to run out of time, so that it will make sure the `FAILED` request is sent, even if your lambda's timeout is improperly configured.
