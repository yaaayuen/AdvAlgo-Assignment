"""Pre-defined courses and prerequisites for the course system"""
from course import Course, Level
from graph import Graph

MAX_COURSES = 10

COURSES = [
    Course("CS101", "Programming Fundamentals", 4, Level.CORE,
           "Variables, loops. functions and basic problem solving"),
    Course("MA101", "Discrete Mathematics", 3, Level.CORE,
           "Logic, sets, relations and the basics of graph theory"),
    Course("CS201", "Data Structures", 4, Level.CORE,
           "Lists, stacks, queues, trees, hash tables and graphs"),
    Course("CS202", "Database Systems", 3, Level.CORE,
           "Relational design, SQL and normalisation"),
    Course("CS301", "Algorithms", 4, Level.CORE,
           "Sorting, searching, graph algorithms and complexity"),
    Course("CS302", "Software Engineering", 3, Level.CORE,
           "Requirements, design, testing and teamwork"),
    Course("CS303", "Web Development", 3, Level.ELECTIVE,
           "HTML, CSS, JavaScript and server-side basics"),
    Course("CS401", "Artificial Intelligence", 4, Level.ELECTIVE,
           "Search, knowledge representation and machine learning"),
]

# Each pair is (prerequisite, course it unlocks) [prerequisite -> course]
PREREQUISITES = [
    ("CS101", "CS201"), ("CS101", "CS202"),
    ("CS201", "CS301"), ("MA101", "CS301"),
    ("CS201", "CS302"), ("CS202", "CS302"),
    ("CS202", "CS303"), ("CS301", "CS401"),
]


def build_course_system():
    """Return (graph, courses) filled with every pre-defined course and prerequisite"""
    graph = Graph()
    courses = {}
    for course in COURSES:
        graph.add_vertex(course.code)
        courses[course.code] = course
    for prerequisite, course_code in PREREQUISITES:
        graph.add_edge(prerequisite, course_code)
    return graph, courses


if __name__ == "__main__":
    graph, courses = build_course_system()
    print(f"{len(courses)} courses loaded (maximum {MAX_COURSES})")
    for code in graph.vertices():
        print(" ", courses[code])

    needs = sorted(graph.list_incoming_adjacent_vertex("CS301"))
    print("\nCS301 needs:", [str(courses[code]) for code in needs])
    unlocks = sorted(graph.list_outgoing_adjacent_vertex("CS101"))
    print("CS101 unlocks:", [str(courses[code]) for code in unlocks])
