class WorkoutGenerator:
    """
    Ein einfacher Trainingsplan-Generator, der Übungen basierend auf Muskelgruppen erstellt.
    """

    # Vordefinierte Muskelgruppen und dazugehörige Übungen
    muscle_groups = {
        "chest": ["Bench Press", "Push Ups", "Chest Fly"],
        "back": ["Deadlift", "Pull Ups", "Lat Pulldown"],
        "legs": ["Squat", "Lunges", "Leg Press"],
        "shoulders": ["Shoulder Press", "Lateral Raise"],
        "arms": ["Biceps Curl", "Triceps Extension", "Hammer Curl"]
    }

    def generate_plan(self, days: int = 3):
        """
        Erstellt einen Trainingsplan für eine bestimmte Anzahl von Tagen.

        Parameter:
            days (int): Anzahl der Trainingstage. Standardwert ist 3.

        Ablauf:
            - Wählt für jeden Tag eine Muskelgruppe aus.
            - Die Auswahl erfolgt zyklisch, falls die Anzahl der Tage die Anzahl
              der verfügbaren Muskelgruppen übersteigt.
            - Jeder Tag enthält die zugehörige Muskelgruppe und die empfohlenen Übungen.

        Rückgabe:
            dict: Ein strukturierter Trainingsplan im Format:
                {
                    "Day 1": {
                        "muscle_group": "chest",
                        "exercises": [...]
                    },
                    ...
                }
        """

        plan = {}
        group_names = list(self.muscle_groups.keys())

        for i in range(days):
            # Muskelgruppe zyklisch auswählen
            group = group_names[i % len(group_names)]

            # Trainingsplan für den jeweiligen Tag definieren
            plan[f"Day {i+1}"] = {
                "muscle_group": group,
                "exercises": self.muscle_groups[group]
            }

        return plan
