from observers import (
    ProcessingSubject,
    ProgressObserver,
    ErrorObserver
)


def test_observer_notifications(capsys):
    subject = ProcessingSubject()

    progress = ProgressObserver()
    error = ErrorObserver()

    subject.attach(progress)
    subject.attach(error)

    subject.notify("Dataset processing started.")

    captured = capsys.readouterr()

    assert "[PROGRESS] Dataset processing started." in captured.out
    assert "[ERROR] Dataset processing started." in captured.out


def test_attach_and_detach_observer(capsys):
    subject = ProcessingSubject()

    progress = ProgressObserver()

    subject.attach(progress)
    subject.notify("Processing started.")

    subject.detach(progress)
    subject.notify("Processing completed.")

    captured = capsys.readouterr()

    assert "[PROGRESS] Processing started." in captured.out
    assert "[PROGRESS] Processing completed." not in captured.out


def test_duplicate_observer_is_not_registered_twice(capsys):
    subject = ProcessingSubject()

    progress = ProgressObserver()

    subject.attach(progress)
    subject.attach(progress)

    subject.notify("Testing notification.")

    captured = capsys.readouterr()

    assert captured.out.count("[PROGRESS]") == 1
