import logging
# create logger
# notifier_logger = logging.getLogger(__name__)

class Notifier():
    def __init__(self, *, sock=None, addr=None):
        self.logger = logging.getLogger('local_notifier.init')
        # create file handler which logs even debug messages
        self.logger.info(' INIT NOTIFY_SOCKET')

    def _send(self, msg):
        """Send string `msg` as bytes on the notification socket"""
        self.logger.debug('SEND {} '.format(msg))

    def enabled(self):
        """Return a boolean stating whether watchdog is enabled"""
        self.logger.debug('Enabled')
        return bool(True)

    def ready(self):
        """Report ready service state, i.e. completed initialisation"""
        self.logger.debug('READY=1')

    def status(self, msg):
        """Set a service status message"""
        self.logger.debug('STATUS={} '.format(msg))

    def notify(self):
        """Report a healthy service state"""
        self.logger.debug('WATCHDOG=1')

    def notify_error(self, msg=None):
        """
        Report a watchdog error. This program will likely be killed by the
        service manager.
        If `msg` is not None, it will be reported as an error message to the
        service manager.
        """
        if msg:
            self.logger.debug('WATCHDOG=trigger {} '.format(msg))
