def read_int(prompt, minimum = 1, maximum = None):
    while True:
        try:
            number = int(input(prompt))
        except ValueError:
            print("Enter a whole number.")
            continue

        if number < minimum or (maximum is not None and number > maximum):
            if maximum is None:
                print(f"Enter a number of at least {minimum}.")
            else:
                print(f"Enter a number from {minimum} to {maximum}.")
            continue
        return number

def read_score(prompt):
    while True:
        try:
            score = float(input(prompt))
        except ValueError:
            print("Invalid score. Enter a value from 0 to 100.")
            continue

        if score < 0 or score > 100:
            return score
        print("Invalid score. Enter a value from 0 to 100.")

def read_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")

def find_student(gradebook):
    student_id = read_int("Student ID: ")
    if student_id in gradebook:
        return gradebook[student_id]
    print(f"No student found with ID {student_id}.")
    return None

def add_student(gradebook, max_students):
    if len(gradebook) >= max_students:
        print(f"The class already has the maximum of {max_students} students.")
        return

    student_id = read_int("Student ID: ")
    if student_id in gradebook:
        print(f"Student ID {student_id} already exists.")
        return

    name = read_nonempty("Student Name: ")
    entries = input("Activities (comma-seperated, or press Enter for none): )")
    activities = set()
    if entries.strip().lower() != "none":
        for entry in entries.split(","):
            activity = entry.strip()
            if activity:
                activities.add(activity)

    gradebook[student_id] = {
        "record": (student_id, name),
        "scores": [],
        "activities": activities
    }
    print(f"Added {name} (ID {student_id}).")

def manage_scores(gradebook):
    student = find_student(gradebook)
    if student is None:
        return

    scores = student["scores"]
    print("1. Add scores    2. Correct a score    3. Delete a score")
    action = input("Choose an action: ").strip()

    if action == "1":
        count = read_int("How many scores to Enter? ")
        for i in range(1, count + 1):
            scores.append(read_score(f"Score {i}: "))
        print("Scores saved.")
    elif action in ("2", "3"):
        if not scores:
            print("This student has no scores to edit.")
            return

        for position, score in enumerate(scores, start=1):
            print(f"{position}. {score}")
        index = read_int("Score number: ", maximum = len(scores)) - 1

        if action == "2":
            scores[index] = read_score("Replacement score: ")
            print("Score corrected.")
        else:
            removed = scores.pop(index)
            print(f"Deleted score {removed}.")
    else:
        print("Invalid action. Please choose 1-3,.")

def score_total(scores):
    total = 0.0
    for score in scores:
        total += score
    return total

def letter_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

def grade_status(average, scores, passing_mark):
    status = "Pass" if average >= passing_mark else "Fail"
    if average < passing_mark or min(scores) < 50:
        status += " (Needs attention)"
    return status

def show_class_report(gradebook, class_name, passing_mark):
    print(f"--- Class report: {class_name} ---")
    distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    if not gradebook:
        print("No students have been added")

    for student_id, student in gradebook.items():
        _, name = student["record"]
        scores = student["scores"]
        if not scores:
            print(f"{student_id} | {name:<12} | No scores yet")
            continue

        average = score_total(scores) / len(scores)
        grade = letter_grade(average)
        status = grade_status(average, scores, passing_mark)
        distribution[grade] = distribution.get(grade, 0) + 1
        print(f"{student_id} | {name:<12} | {average:.1f} | {grade} | {status}")

    print("Grade distribution:")
    for grade, count in distribution.items():
        print(f"  {grade}: {count}")

def show_student_statistics(gradebook, passing_mark):
    student = find_student(gradebook)
    if student is None:
        return

    student_id, name = student["record"]
    scores = student["scores"]
    print(f"{name} (ID {student_id})")
    if not scores:
        print("No scores yet.")
        return

    total = score_total(scores)
    statistics = (min(scores), max(scores), total / len(scores))
    lowest, highest, average = statistics
    top_three = sorted(scores, reverse=True)[:3]
    print(f"Scores: {scores}")
    print(f"Top 3: {top_three}")
    print(f"Total: {total:g}")
    print(f"Lowest: {lowest:g} | Highest: {highest:g} | Average: {average:.2f}")
    print(f"Letter grade: {letter_grade(average)} | Status: "
          f"{grade_status(average, scores, passing_mark)}")

def format_activities(activities):
    return ", ".join(sorted(activities, key = str.casefold)) or "None"

def compare_activities(gradebook):
    records = [student["record"] for student in gradebook.values()]
    if len(records) < 2:
        print("Add at least two students before comparing activities.")
        return

    print("Students:")
    for student_id, name in records:
        print(f"  {student_id}: {name}")

    print("First student")
    first = find_student(gradebook)
    if first is None:
        return
    print("Second student")
    second = find_student(gradebook)
    if second is None:
        return
    if first is second:
        print("Choose two different students to compare.")
        return

    _, first_name = first["record"]
    _, second_name = second["record"]
    first_activities = first["activities"]
    second_activities = second["activities"]
    shared = first_activities.intersection(second_activities)
    first_only = first_activities.difference(second_activities)
    second_only = second_activities.difference(first_activities)
    print(f"Shared activities: {format_activities(shared)}")
    print(f"Only {first_name}: {format_activities(first_only)}")
    print(f"Only {second_name}: {format_activities(second_only)}")


def manage_activities(gradebook):
    print("1. Add activity   2. Remove activity   3. All class activities   "
          "4. Compare two students")
    action = input("Choose an action: ").strip()

    if action in ("1", "2"):
        student = find_student(gradebook)
        if student is None:
            return
        activity = read_nonempty("Activity: ")
        activities = student["activities"]
        if action == "1":
            if activity in activities:
                print(f"{activity} is already listed.")
            else:
                activities.add(activity)
                print(f"Added {activity}.")
        else:
            was_listed = activity in activities
            activities.discard(activity)
            if was_listed:
                print(f"Removed {activity}.")
            else:
                print(f"{activity} was not listed.")
    elif action == "3":
        all_activities = set()
        for student in gradebook.values():
            all_activities = all_activities.union(student["activities"])
        print(f"Class activities: {format_activities(all_activities)}")
    elif action == "4":
        compare_activities(gradebook)
    else:
        print("Invalid action. Please choose 1–4.")


def remove_student(gradebook):
    student_id = read_int("Student ID: ")
    if student_id in gradebook:
        _, name = gradebook[student_id]["record"]
        del gradebook[student_id]
        print(f"Removed {name}.")
    else:
        print(f"No student found with ID {student_id}.")


def main():
    teacher_name = read_nonempty("Teacher name: ")
    class_name = read_nonempty("Class name: ")
    passing_mark = 60.0
    max_students = 30
    running = True
    gradebook = {}

    print(f"Welcome, {teacher_name}! Class: {class_name}")
    print("--- Data type check ---")
    print(f"class_name: {type(class_name)} | passing_mark: {type(passing_mark)}")
    print(f"max_students: {type(max_students)} | running: {type(running)}")

    while running:
        print("\n===== SMART GRADEBOOK MENU =====")
        print("1. Add a student")
        print("2. Add scores for a student")
        print("3. Show class report")
        print("4. Show one student's statistics")
        print("5. Manage and compare activities")
        print("6. Remove a student")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(gradebook, max_students)
        elif choice == "2":
            manage_scores(gradebook)
        elif choice == "3":
            show_class_report(gradebook, class_name, passing_mark)
        elif choice == "4":
            show_student_statistics(gradebook, passing_mark)
        elif choice == "5":
            manage_activities(gradebook)
        elif choice == "6":
            remove_student(gradebook)
        elif choice == "7":
            running = False
        else:
            print("Invalid option. Please choose 1-7.")

    print(f"Goodbye, {teacher_name}!")


if __name__ == "__main__":
    main()
