filename = "wordle_guesses.txt"

with open(filename, "r", encoding="utf-8-sig") as file:
    words = {
        line.strip().upper()
        for line in file
        if len(line.strip()) == 5
    }

with open(filename, "w", encoding="utf-8") as file:
    for word in sorted(words):
        file.write(word + "\n")

print(f"{len(words)} unique words saved")
