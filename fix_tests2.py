with open("tests/test_app.py", "r") as f:
    lines = f.read().splitlines()
# Find line with test_chat_distinct_answers (0-indexed)
start_idx = None
for i, line in enumerate(lines):
    if line.startswith("def test_chat_distinct_answers"):
        start_idx = i
        break
if start_idx is not None:
    # Replace from start_idx through start_idx+4 (the 5 original lines)
    new_lines = [
        "def test_chat_distinct_answers(client):",
        '    r1 = client.post("/api/chat", json={"message":"Who won 2024 Drivers Championship?"})',
        '    r2 = client.post("/api/chat", json={"message":"Show 2023 season highlights"})',
        '    r3 = client.post("/api/chat", json={"message":"Who won 2022 Constructors Championship?"})',
        '    a = r1.get_json()["result"]["answer"]',
        '    b = r2.get_json()["result"]["answer"]',
        '    c = r3.get_json()["result"]["answer"]',
        '    assert a != b and b != c',
    ]
    # Find the line after original block (original has 5 lines: def + 3 a,b,c + assert)
    end_idx = start_idx + 5
    lines[start_idx:end_idx] = new_lines
    with open("tests/test_app.py", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("fixed at line", start_idx)
else:
    print("not found")
