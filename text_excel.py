import pandas as pd

# 1️⃣ Read your text file
with open(r"D:\Varath\ai_data_copilot\ai_data_copilot\bank_report.txt", "r") as file:
    lines = file.readlines()

# 2️⃣ Convert structured text into rows
data = []
record = {}
for line in lines:
    line = line.strip()
    if not line:
        if record:
            data.append(record)
            record = {}
        continue
    if ":" in line:
        key, value = line.split(":", 1)
        record[key.strip()] = value.strip()

if record:
    data.append(record)

# 3️⃣ Create DataFrame
df = pd.DataFrame(data)

# 4️⃣ Save to Excel and CSV
df.to_excel("transactions.xlsx", index=False)
df.to_csv("transactions.csv", index=False)

print("✅ Conversion completed. Files saved locally.")