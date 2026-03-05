# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose
Glitchy Guesser is a number guessing game built with Streamlit. The player selects a difficulty (Easy, Normal, or Hard), which sets the secret number's range and the number of allowed attempts. Each guess receives a hint — "Go HIGHER!" or "Go LOWER!" — to guide the player toward the secret number. The goal is to guess correctly before running out of attempts, with a score that decreases the more guesses it takes.

### Bugs Found

| # | Bug | Location |
|---|-----|----------|
| 1 | Hints were backwards — "Go HIGHER!" shown when guess was too high | `check_guess` in `app.py` |
| 2 | New Game button did nothing after a win or loss | New game handler in `app.py` |
| 3 | Submit button required two clicks to register | `st.text_input` + `st.button` in `app.py` |
| 4 | Attempts left counter started at 7 instead of 8 on Normal | Session state init in `app.py` |
| 5 | Normal and Hard difficulty ranges were swapped | `get_range_for_difficulty` in `app.py` |
| 6 | New Game always picked a secret from 1–100 regardless of difficulty | New game handler in `app.py` |
| 7 | Switching difficulty didn't reset the game state | Session state management in `app.py` |

### Fixes Applied

1. **Swapped hint messages** in `check_guess` — paired "Go LOWER!" with `guess > secret` and "Go HIGHER!" with `guess < secret`.
2. **Added `st.session_state.status = "playing"`** (and history reset) to the New Game handler so the game unblocks after a win or loss.
3. **Wrapped text input and submit button in `st.form`** so both are submitted atomically in a single rerun, eliminating the double-click issue.
4. **Changed `st.session_state.attempts` init from `1` to `0`** so the attempts left display is accurate from the start.
5. **Swapped Normal and Hard return values** in `get_range_for_difficulty` — Normal is now 1–50, Hard is 1–100.
6. **Replaced hardcoded `random.randint(1, 100)`** in the New Game handler with `random.randint(low, high)` to respect the selected difficulty.
7. **Added difficulty change detection** using `st.session_state.difficulty` — switching difficulty now fully resets the game state.
8. **Refactored `check_guess` into `logic_utils.py`** and added a `conftest.py` at the project root so pytest can find the module.
9. **Fixed existing pytest tests** to unpack the `(outcome, message)` tuple returned by `check_guess`, and added two new tests specifically targeting the swapped hint message bug.

## 📸 Demo

- [ ] [Winning game screenshot](success.png)

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
