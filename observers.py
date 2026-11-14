from abc import ABC, abstractmethod


class ProcessingObserver(ABC):
    """
    Abstract interface for processing observers.
    """

    @abstractmethod
    def update(self, message):
        pass


class ProgressObserver(ProcessingObserver):
    """
    Displays dataset processing progress.
    """

    def update(self, message):
        print(f"[PROGRESS] {message}")


class ErrorObserver(ProcessingObserver):
    """
    Displays processing error messages.
    """

    def update(self, message):
        print(f"[ERROR] {message}")


class ProcessingSubject:
    """
    Manages observers and notifies them about events.
    """

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """Registers an observer."""

        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Removes a registered observer."""

        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, message):
        """Notifies all registered observers."""

        for observer in self._observers:
            observer.update(message)
