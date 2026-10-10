"""Menu-driven university course prerequisite system"""
from unicodedata import decimal

from course import Course, Level
from course_data import build_course_system, MAX_COURSES

def read_course_code(prompt, courses):
    """Keeps asking until the user types the code of an existing course, blank input returns None"""
    while True:
        code = input(prompt).strip().upper()
        if code == "":
            return None
        if code in courses:
            return code
        print(f"Course {code} not found. Choose from: {', '.join(sorted(courses))}")


def read_text(prompt):
    """Ask until the user types something that is not blank"""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("This field cannot be empty")


def read_positive_int(prompt):
    """Ask until the user types a whole number greater than o"""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number")
            continue
        if value > 0:
            return value
        print("Please enter a number greater than 0")


def read_level(prompt):
    """Ask until the user picks C (Core) or E (Elective)"""
    while True:
        choice = input(prompt).strip().upper()
        if choice == "C":
            return Level.CORE
        if choice == "E":
            return Level.ELECTIVE
        print("Please enter 'C' for Core or 'E' for Elective")


def course_lines(codes, courses):
    """Turn a list of codes into sorted lines"""
    return [f"- {code} ({courses[code].name})" for code in sorted(codes)]


def print_menu():
    """Show the menu options"""
    print("==== University Course Prerequisite System ====")
    print("1. View All Courses")
    print("2. View Course Details")
    print("3. View Prerequisites of a Course")
    print("4. View Courses Unlocked by a Course")
    print("5. Add Course")
    print("6. View Course Profile")
    print("9. Exit")


def view_all_courses(graph, courses):
    """List every course's code and name"""
    print("\nAvailable Courses:")
    for number, code in enumerate(graph.vertices(), start=1):
        print(f"{number}. {courses[code]}")
    print()


def view_course_details(graph, courses):
    """Show every detail of one course"""
    code = read_course_code("Enter Course Code (blank to cancel): ", courses)
    if code is None:
        return
    print(courses[code].full_details())
    print()


def view_prerequisites(graph, courses):
    """List the incoming edges (prerequisites) of one course"""
    code = read_course_code("Enter Course Code: (blank to cancel): ", courses)
    if code is None:
        return
    prerequisites = graph.list_incoming_adjacent_vertex(code)
    print(f"Prerequisites for {courses[code]}:")
    print("\n".join(course_lines(prerequisites, courses)) or "- None")
    print()


def view_unlocked(graph, courses):
    """List the outgoing edges (unlocked) of one course"""
    code = read_course_code("Enter Course Code (blank to cancel): ", courses)
    if code is None:
        return
    unlocked = graph.list_outgoing_adjacent_vertex(code)
    print(f"Courses unlocked by {courses[code]}:")
    print("\n".join(course_lines(unlocked, courses)) or "- None")
    print()


def add_course(graph, courses):
    """Create a new course and add it to the graph"""
    if len(courses) >= MAX_COURSES:
        print(f"Cannot add: the system already has the maximum of {MAX_COURSES} courses\n")
        return

    code = input("Enter new Course Code (blank to cancel): ").strip().upper()
    if code == "":
        return
    if not code.isalnum():
        print("Course code must contain letters and digits only\n")
        return
    if code in courses:
        print(f"Course {code} is already in the system\n")
        return

    name = read_text("Enter Course Name: ")
    credit_hours = read_positive_int("Enter Credit Hours: ")
    level = read_level("Core or Elective? (C/E): ")
    description = input ("Enter Course Description (optional): ").strip()

    course = Course(code, name, credit_hours, level, description)
    graph.add_vertex(course.code)
    courses[course.code] = course
    print(f"Added {course}. Use option 7 to add its prerequisites\n")


def view_course_profile(graph, courses):
    """Show a course profile: electives show name only, core shows everything"""
    code = read_course_code("Enter Course Code (blank to cancel): ", courses)
    if code is None:
        return
    print(courses[code].profile())
    print()


def main():
    """Build the course system, run the menu"""
    graph, courses = build_course_system()

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()
        if choice == "1":
            view_all_courses(graph, courses)
        elif choice == "2":
            view_course_details(graph, courses)
        elif choice == "3":
            view_prerequisites(graph, courses)
        elif choice == "4":
            view_unlocked(graph, courses)
        elif choice == "5":
            add_course(graph, courses)
        elif choice == "6":
            view_course_profile(graph, courses)
        elif choice == "9":
            print("Exiting program...")
            break
        else:
            print("Please enter a valid menu number")


if __name__ == "__main__":
    main()