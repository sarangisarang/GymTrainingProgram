class WorkoutGenerator:
    """
    Simple workout generator based on muscle groups.
    """

    muscle_groups = {
        "chest": ["Bench Press", "Push Ups", "Chest Fly"],
        "back": ["Deadlift", "Pull Ups", "Lat Pulldown"],
        "legs": ["Squat", "Lunges", "Leg Press"],
        "shoulders": ["Shoulder Press", "Lateral Raise"],
        "arms": ["Biceps Curl", "Triceps Extension", "Hammer Curl"]
    }

    def generate_plan(self, days: int = 3):
        """
        Generate workout plan for given number of days.
        """
        plan = {}
        group_names = list(self.muscle_groups.keys())

        for i in range(days):
            group = group_names[i % len(group_names)]
            plan[f"Day {i+1}"] = {
                "muscle_group": group,
                "exercises": self.muscle_groups[group]
            }

        return plan