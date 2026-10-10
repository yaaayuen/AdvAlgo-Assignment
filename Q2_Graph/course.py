"""Course entity for the course-prerequisite system"""
from enum import Enum

class Level (Enum):
    """Whether a course is compulsory or elective"""
    CORE = "Core"
    ELECTIVE = "Elective"


class Course:
    """One university course"""
    def __init__(self, code, name, credit_hours, level, description=""):
        code = code.strip().upper()
        if not code:
            raise ValueError("Course code cannot be empty")
        if not name.strip():
            raise ValueError("Course name cannot be empty")
        if not isinstance(credit_hours, int) or credit_hours <= 0:
            raise ValueError("Credit hours must be a positive whole number")
        if not isinstance(level, Level):
            raise ValueError("Level must be Level.CORE or Level.ELECTIVE")

        self.code = code
        self.name = name.strip()
        self.credit_hours = credit_hours
        self.level = level
        self.description = description


    def is_elective(self):
        """Return TRUE if the course is elective"""
        return self.level is Level.ELECTIVE


    def full_details(self):
        """Return every detail, whatever the level (mandatory feature b)"""
        lines = [f"Code: {self.code}",
                 f"Name: {self.name}",
                 f"Credit hours: {self.credit_hours}",
                 f"Level: {self.level.value}"]
        if self.description:
            lines.append(f"Description: {self.description}")
        return "\n".join(lines)


    def profile(self):
        """Advanced feature b: electives show only the name, core shows everything"""
        if self.is_elective():
            return f"Name: {self.name} (elective: other details are hidden)"
        return self.full_details()


    def __str__(self):
        return f"{self.code} - {self.name}"


    def __repr__(self):
        return f"Course({self.code!r})"


if __name__ == "__main__":
    ds = Course("cs201 ", "Data Structures", 4, Level.CORE,
                "Lists, stacks, queues, trees, hash tables and graphs")
    web = Course("CS303", "Web Development", 3, Level.ELECTIVE)

    print(ds)
    print(repr(ds))
    print("\n--- Full details (elective) ---")
    print(web.full_details())
    print("\n--- Profile (core) ---")
    print(ds.profile())
    print("\n--- Profile (elective) ---")
    print(web.profile())

    for bad in [("", "X", 3, Level.CORE), ("CS999", "X", 0, Level.CORE),
                ("CS999", "X", 3, "Core")]:
        try:
            Course(*bad)
        except ValueError as error:
            print("Rejected:", error)