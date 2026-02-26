with open("data.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

cleaned = [line.strip().strip('"') + "\n" for line in lines]

with open("data.csv", "w", encoding="utf-8") as f:
    f.writelines(cleaned)

print("CSV cleaned successfully.")