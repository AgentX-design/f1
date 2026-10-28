with open("tests/test_app.py", "r") as f:
    text = f.read()
old_block = "def test_chat_distinct_answers(client):\n    a = client.post('/api/chat', json={'message':'Who won 2024 Drivers Championship?'}).get_json()['result']['answer']\n    b = client.post('/api/chat', json={'message':'Show 2023 season highlights'}).get_json()['result']['answer']\n    c = client.post('/api/chat', json={'message':'Who won 2022 Constructors Championship?'}).get_json()['result']['answer']\n    assert a != b and b != c"
new_block = "def test_chat_distinct_answers(client):\n    r1 = client.post('/api/chat', json={'message':'Who won 2024 Drivers Championship?'})\n    r2 = client.post('/api/chat', json={'message':'Show 2023 season highlights'})\n    r3 = client.post('/api/chat', json={'message':'Who won 2022 Constructors Championship?'})\n    a = r1.get_json()['result']['answer']\n    b = r2.get_json()['result']['answer']\n    c = r3.get_json()['result']['answer']\n    assert a != b and b != c"
if old_block in text:
    text = text.replace(old_block, new_block)
    with open("tests/test_app.py", "w") as f:
        f.write(text)
    print("fixed")
else:
    print("not found; lines checked")
