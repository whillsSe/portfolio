def calculate_priority(importance, days_until_due):
    """
    Calculate the priority score based on importance and days until the task is due.

    Parameters:
    - importance (int): The importance level of the task (0-3).
    - days_until_due (int): Days remaining until the task is due. Negative if overdue.

    Returns:
    - priority (float): The calculated priority score.
    """

    # If importance is 0, return the lowest priority
    if importance == 0:
        return 0
    
    # If due today or overdue, return very high priority
    if days_until_due <= 0:
        return 1000 + importance  # +importance to give higher priority to tasks with higher importance

    # Else, calculate based on importance and days_until_due
    priority = importance / days_until_due

    return priority

if __name__ == "__main__":
    # Get input from user
    importance = int(input("Enter the importance level (0-3): "))
    days_until_due = int(input("Enter the number of days until the task is due (negative if overdue): "))

    # Calculate priority and print result
    print(f"Calculated Priority: {calculate_priority(importance, days_until_due)}")
