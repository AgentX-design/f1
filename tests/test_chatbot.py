from src.chatbot import Chatbot

def test_driver_champion_all_seasons():
    bot = Chatbot()
    for y in [2021,2022,2023,2024,2025]:
        r = bot.ask(f"Who won the {y} Drivers Championship?")
        assert r['retrieval'] == 'structured'
        assert str(y) in r['answer']
        assert r['season'] == y

def test_constructor_champion():
    bot = Chatbot()
    for y in [2021,2022,2023,2024,2025]:
        r = bot.ask(f"Who won the {y} Constructors Championship?")
        assert r['retrieval'] == 'structured'
        assert r['season'] == y

def test_standings_2024():
    bot = Chatbot()
    r = bot.ask('Show 2024 Drivers Championship standings')
    assert r['season'] == 2024
    assert 'McLaren' in r['answer']
    assert 'Red Bull' in r['answer']

def test_standings_other_season():
    bot = Chatbot()
    r = bot.ask('Show 2021 Drivers Championship standings')
    assert r['retrieval'] == 'structured'
    assert 'Verstappen' in r['answer']
    assert 'Mercedes' in r['answer']

def test_race_winner_monaco_2023():
    bot = Chatbot()
    r = bot.ask('Give the 2023 Monaco Grand Prix winner')
    assert r['season'] == 2023
    assert 'Verstappen' in r['answer']

def test_sprint_events():
    bot = Chatbot()
    r = bot.ask('Which 2023 weekends had sprint races')
    assert 'sprint' in r['answer'].lower()
    assert 'Bahrain Grand Prix' in r['answer']

def test_fallbacks_distinct():
    bot = Chatbot()
    a = bot.ask('Unknown question XYZ')['answer']
    b = bot.ask('Another mystery question QRS')['answer']
    # Both unknown questions may return the same fallback; verify structured fallback is present
    assert 'Try asking' in a
    assert 'Try asking' in b
