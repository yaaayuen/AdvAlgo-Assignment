"""Menu-driven university course prerequisite system"""
from course_data import build_course_system

def read_course_code(prompt, courses):
    """Keeps asking until the user types the code of an existing course"""
    while True:
        code = input(prompt).strip().upper()
        if code in courses:
            return code
        print(f"Course {code} not found. Choose from: {', '.join(sorted(courses))}")


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
    print("9. Exit")


def view_all_courses(graph, courses):
    """List every course's code and name"""
    print("\nAvailable Courses:")
    for number, code in enumerate(graph.vertices(), start=1):
        print(f"{number}. {courses[code]}")
    print()


def view_course_details(graph, courses):
    """Show every detail of one course"""
    code = read_course_code("Enter Course Code: ", courses)
    print(courses[code].full_details())
    print()


def view_prerequisites(graph, courses):
    """List the incoming edges (prerequisites) of one course"""
    code = read_course_code("Enter Course Code: ", courses)
    prerequisites = graph.list_incoming_adjacent_vertex(code)
    print(f"Prerequisites for {courses[code]}:")
    print("\n".join(course_lines(prerequisites, courses)) or "- None")
    print()


def view_unlocked(graph, courses):
    """List the outgoing edges (unlocked) of one course"""
    code = read_course_code("Enter Course Code: ", courses)
    unlocked = graph.list_outgoing_adjacent_vertex(code)
    print(f"Courses unlocked by {courses[code]}:")
    print("\n".join(course_lines(unlocked, courses)) or "- None")
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
        elif choice == "9":
            print("Exiting program...")
            break
        else:
            print("Please enter a valid menu number")


if __name__ == "__main__":
    main()