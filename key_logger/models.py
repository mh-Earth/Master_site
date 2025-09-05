from django.db import models

class Keystroke(models.Model):
    """
    A model to store individual keystrokes.

    Each keystroke is associated with a timestamp and a session ID to
    group keystrokes from a single logging session.
    """
    username = models.CharField(max_length=100)    
    # CharField to store the captured keystroke. This could be a single
    # character, a special key name (e.g., 'Enter'), or a combination.
    keystroke = models.CharField(max_length=50)

    # DateTimeField to record the exact time the key was pressed.
    # auto_now_add=True automatically sets the date and time when the object is created.
    timestamp = models.DateTimeField(auto_now_add=True)

    # CharField to store a unique session identifier. This is useful for
    # separating keystrokes from different logging sessions or machines.
    session_id = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a human-readable string representation of the keystroke.
        """
        return f'[{self.timestamp}] - Session {self.session_id}: {self.username}'
