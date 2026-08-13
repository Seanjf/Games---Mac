answers = set()

with open("wordle_answers.txt", "r", encoding="utf-8-sig") as file:
    answers = {line.strip().upper() for line in file}

guesses = set()

with open("wordle_guesses.txt", "r", encoding="utf-8-sig") as file:
    guesses = {line.strip().upper() for line in file}

duplicates = answers.intersection(guesses)

print("Words appearing in both lists:", len(duplicates))
