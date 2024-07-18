import time
from itertools import permutations
from constraint import Problem, AllDifferentConstraint


def get_input(prompt):
    while True:
        term = input(prompt).strip().upper()
        if term.isalpha():
            return term
        print("Invalid input. Please enter a word consisting of letters only.")


def get_unique_letters(first_term, second_term, result):
    return "".join(set(first_term + second_term + result))


def word_to_number(word, mapping):
    return sum(mapping[char] * (10**idx) for idx, char in enumerate(reversed(word)))


def create_constraints(first_term, second_term, result, unique_letters):
    def constraint(*args):
        mapping = dict(zip(unique_letters, args))
        return word_to_number(first_term, mapping) + word_to_number(
            second_term, mapping
        ) == word_to_number(result, mapping)

    return constraint


def solve_cryptarithm(first_term, second_term, result):
    unique_letters = get_unique_letters(first_term, second_term, result)
    problem = Problem()

    problem.addVariables(unique_letters, range(10))
    problem.addConstraint(AllDifferentConstraint(), unique_letters)
    problem.addConstraint(lambda x: x != 0, first_term[0])
    problem.addConstraint(lambda y: y != 0, second_term[0])

    problem.addConstraint(
        create_constraints(first_term, second_term, result, unique_letters),
        unique_letters,
    )

    return problem.getSolutions()


def ask_for_variables():
    first_term = get_input("Input first term: ")
    second_term = get_input("Input second term: ")
    result = get_input("Input result: ")

    start_time = time.time()
    solutions = solve_cryptarithm(first_term, second_term, result)
    end_time = time.time()

    print(f"\nExecution time: {end_time - start_time} seconds")

    if solutions:
        for solution in solutions:
            print(
                f"Valid mapping found: {word_to_number(first_term, solution)} + {word_to_number(second_term, solution)} = {word_to_number(result, solution)}"
            )
        if (
            input("\nFound valid combination. Do you want to continue? (yes/no): ")
            .strip()
            .lower()
            == "yes"
        ):
            ask_for_variables()
        else:
            print("Program ended.")
    else:
        if (
            input("\nNo valid combination found. Do you want to try again? (yes/no): ")
            .strip()
            .lower()
            == "yes"
        ):
            ask_for_variables()
        else:
            print("Program ended.")


ask_for_variables()
