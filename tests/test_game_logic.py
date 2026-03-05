from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# Bug fix tests: messages were swapped — "Go HIGHER!" appeared when guess was too high,
# and "Go LOWER!" appeared when guess was too low. These tests would have caught that bug.
def test_too_high_message_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' hint when guess is too high, got: '{message}'"

def test_too_low_message_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' hint when guess is too low, got: '{message}'"
