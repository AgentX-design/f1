with open("src/chatbot.py") as f:
    text = f.read()
marker = "# Race winners (sampled)"
if marker not in text:
    print("marker not found")
    exit(0)
qualifying = '''        # Qualifying / pole (check before race winner when requested)
        if ("qualifying" in msg or "pole" in msg or "grid" in msg) and y is not None:
            gp = "British Grand Prix"
            for alias, canonical in SAMPLE_GP_ALIASES.items():
                if alias in msg:
                    gp = canonical; break
            note = self.data.qualifying_note(y, gp)
            return {
                "answer": f"{y} qualifying note: {note}.",
                "sources": sources,
                "season": y,
                "retrieval": "structured",
                "retrieval_results": [{"season": y, "gp": gp, "category": "qualifying_note"}],
            }
'''
# Replace marker occurrence with qualifying block + marker
text = text.replace("# Race winners (sampled)", qualifying + "\n        # Race winners (sampled)", 1)
with open("src/chatbot.py", "w") as f:
    f.write(text)
print("qualifying block inserted before race winner")
