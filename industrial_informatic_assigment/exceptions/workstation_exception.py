class WorkstationError(Exception):
    def __init__(self, msg='Something went wrong when communicating with the workstation!', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
