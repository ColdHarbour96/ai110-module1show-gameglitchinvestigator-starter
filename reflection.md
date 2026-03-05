# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

### Bugs Found and Fixed

**Bug 1: Hints were backwards (`app.py`, `check_guess`)**
When the guess was too high, the game said "Go HIGHER!" and when the guess was too low it said "Go LOWER!" — the opposite of what it should say. The `>` comparison was correct but the messages were swapped. Fixed by pairing "Go LOWER!" with `guess > secret` and "Go HIGHER!" with `guess < secret`.

**Bug 2: New Game button didn't actually reset the game (`app.py`, new game handler)**
After winning or losing, clicking "New Game" appeared to do nothing. The handler reset `attempts` and `secret` but never reset `st.session_state.status` back to `"playing"`. Because status was still `"won"` or `"lost"`, the app hit `st.stop()` on every rerun and blocked all interaction. Fixed by adding `st.session_state.status = "playing"` (and `st.session_state.history = []`) to the new game handler.

**Bug 3: Submit button required two clicks (`app.py`, guess form)**
Typing a guess and clicking "Submit Guess" sometimes did nothing on the first click. In Streamlit, clicking a button while a text input is focused first blurs the input (triggering a rerun) and then registers the button click on the next rerun — so the form appeared to need two clicks. Fixed by wrapping the text input and submit button in a `st.form`, which submits both atomically in a single rerun.

**Bug 4: Attempts counter started at 1 instead of 0 (`app.py`, session state init)**
On a fresh game load, the "Attempts left" display showed 7 instead of 8 for Normal difficulty. `st.session_state.attempts` was initialized to `1`, so the display `attempt_limit - attempts` subtracted one attempt before the player had guessed anything. Fixed by initializing `attempts` to `0`.

**Bug 5: Normal and Hard difficulty ranges were swapped (`app.py`, `get_range_for_difficulty`)**
Normal difficulty used a range of 1–100 and Hard used 1–50, meaning Hard was actually easier than Normal. Fixed by swapping the return values so Normal is 1–50 and Hard is 1–100, making difficulty scale correctly.

**Bug 6: New Game always generated a secret from 1–100 (`app.py`, new game handler)**
After clicking "New Game", the secret number was always picked with `random.randint(1, 100)` regardless of the selected difficulty. So on Easy or Normal, the secret could be a number outside the stated range. Fixed by using `random.randint(low, high)` where `low` and `high` come from `get_range_for_difficulty`.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic's CLI AI tool) throughout this project to identify and fix bugs. One example of a correct AI suggestion was the double-click submit bug — I described the symptom and Claude Code correctly diagnosed Streamlit's blur/rerun behavior, then refactored the input and button into a `st.form`. I verified it worked by running the app and confirming a single click submitted the guess. One example where I had to guide the AI was when fixing the difficulty ranges — the AI fixed the swap correctly but I still had to manually verify by playing both Normal and Hard to confirm the ranges felt right in practice, since the AI couldn't run the app itself.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed by first running the app manually and reproducing the original symptom, then checking that it no longer occurred after the change. For example, after fixing the hint messages I guessed a number I knew was too high and confirmed it said "Go LOWER!" instead of "Go HIGHER!". I also ran pytest on `tests/test_game_logic.py`, which revealed that the original tests only checked the `outcome` string and would have passed even with the swapped messages — this showed me that tests need to check the right thing, not just that the function runs. Claude Code helped design the two new message-specific tests (`test_too_high_message_says_go_lower` and `test_too_low_message_says_go_higher`) that would have caught the original bug.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing in the original app because Streamlit reruns the entire script from top to bottom on every interaction — including button clicks and text input changes. Without `st.session_state`, `random.randint()` would be called fresh on every rerun, generating a new secret each time. Streamlit "reruns" work like this: every time the user does anything on the page, Streamlit re-executes your whole Python file. `st.session_state` is a dictionary that persists between these reruns, so values stored there survive each re-execution. The fix that stabilized the secret number was wrapping the `random.randint()` call in an `if "secret" not in st.session_state:` check, so the secret is only generated once and then stored.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing tests that check the exact output that could go wrong — not just that a function returns something, but that it returns the right thing. The original tests passed even with the swapped messages bug because they only checked the outcome string, not the message. Next time I work with AI on a coding task I would describe the symptom more precisely upfront, rather than just saying something "isn't working" — the more specific I was (e.g. "the hints are backwards" vs "something is wrong"), the faster Claude Code found the fix. This project showed me that AI-generated code can have subtle logical bugs that look correct at a glance — the comparisons in `check_guess` were right, but the messages attached to them were wrong, which is exactly the kind of mistake that slips through without careful testing.
