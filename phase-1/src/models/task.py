"""
Task model representing a single todo item with ID, Title, Description, and Completion Status.
"""

class Task:
    """
    Represents a single todo item with ID, Title, Description, and Completion Status.
    """

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a new Task instance

        Args:
            id: Unique identifier for the task
            title: Title of the task (required)
            description: Description of the task (optional)
            completed: Completion status (default: False)
        """
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID must be a positive integer")

        if not title or not title.strip():
            raise ValueError("Title must be provided and non-empty")

        self._id = id
        self._title = title.strip()
        self._description = description.strip() if description else ""
        self._completed = bool(completed)

    @property
    def id(self) -> int:
        """Get the task ID"""
        return self._id

    @property
    def title(self) -> str:
        """Get the task title"""
        return self._title

    @property
    def description(self) -> str:
        """Get the task description"""
        return self._description

    @property
    def completed(self) -> bool:
        """Get the completion status"""
        return self._completed

    @title.setter
    def title(self, value: str) -> None:
        """Set the task title"""
        if not value or not value.strip():
            raise ValueError("Title must be provided and non-empty")
        self._title = value.strip()

    @description.setter
    def description(self, value: str) -> None:
        """Set the task description"""
        self._description = value.strip() if value else ""

    @completed.setter
    def completed(self, value: bool) -> None:
        """Set the completion status"""
        self._completed = bool(value)

    def __repr__(self):
        return f"Task(id={self._id}, title='{self._title}', description='{self._description}', completed={self._completed})"

    def __str__(self):
        status = "Complete" if self._completed else "Incomplete"
        return f"[{self._id}] {self._title} - {status}"