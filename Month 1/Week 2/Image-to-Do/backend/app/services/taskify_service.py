# app/services/taskify_service.py

import re
from typing import List

def extract_tasks(text: str) -> List[str]:
    """
    Extracts tasks from given text. Each task is assumed to start with
    a bullet point, number, or a clear separator.

    Args:
        text (str): Text containing potential tasks.

    Returns:
        List[str]: List of extracted tasks.
    """
    # Exemple simple : extraction basée sur des points ou des tirets comme marqueurs
    task_pattern = re.compile(r"[\*\-\•]\s+(.+)")
    tasks = task_pattern.findall(text)

    # Supprime les espaces inutiles autour des tâches
    tasks = [task.strip() for task in tasks if task.strip()]

    return tasks
