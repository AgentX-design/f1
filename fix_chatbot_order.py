with open("src/chatbot.py", "r") as f:
    text = f.read()
# Find the race winner specific GP block and move qualifying before it
race_start = text.find("        # Race winners (specific GP)")
qual_block_start = text.find("        # Qualifying / pole")
# Extract qualifying block (from start to before fallback)
end_qual = text.find("        # Fallback with distinct helpful text")
qual_block = text[qual_block_start:end_qual]
# Remove it from current position
text_before = text[:qual_block_start]
text_after = text[end_qual:]
# Insert before race_start (in text_before)
new_text_before = text_before.replace("        # Race winners (specific GP)", qual_block + "\n        # Race winners (specific GP)")
text = new_text_before + text_after
with open("src/chatbot.py", "w") as f:
    f.write(text)
print("reordered qualifying before race winners")
