# Constants and preset texts
FONT = ("Segoe UI", 9)
COLPAD = 6

# Category error preset messages
CATEGORY_PRESETS = [
    "Main category is incorrect",
    "Subcategory is incorrect",
    "Custom (write below)"
]

# Noise level error preset messages
NOISE_PRESETS = [
    "Noise level was assessed incorrectly, should have been higher.",
    "Noise level was assessed incorrectly, should have been lower.",
    "Custom (write below)"
]

# Punctuation preset error messages
PUNCT_PRESETS = [
    "since there was no brief pause during speech, there should not be a comma in the transcript.",
    "since there was no pause of at least one second during speech, there should not be an ellipsis in the transcript.",
    "since there was a brief pause after this word during speech, a comma should have been added to the transcript.",
    "since there was a pause of at least one second after this word during speech, an ellipsis should have been added to the transcript.",
    "Custom (write below)"
]

# Spelling preset error messages
SPELL_PRESETS = [
    "This word is misspelled.",
    "Capitalization usage is incorrect.",
    "Spelling error, the correct word should have been used.",
    "Custom (write below)"
]

# Word issues preset error messages
WORD_PRESETS = [
    "this word was spoken during the conversation but is not included in the transcript.",
    "this word was not spoken during the conversation but appears in the transcript.",
    "Custom (write below)"
]

# SBQ (Send Back to Queue) reasons
SBQ_REASONS = [
    "Not Natural (Reading) - Sounds like reading from text",
    "Not Natural (AI-like) - Contains AI-typical requests/conversations", 
    "Wrong Location - Video location doesn't match selected category",
    "Inappropriate Content - Contains harmful/offensive/NSFW content",
    "Category Confusion - Task fits multiple categories, unclear classification",
    "Custom (write below)"
]

# Score-based feedback templates (without SBQ options)
FEEDBACK_TEMPLATES = {
    "5/5": {
        "intro": "Great job! Your recording and transcription are spot-on!",
        "issues": "No issues detected, everything looks perfect.",
        "outro": "Keep up the excellent work!"
    },
    "4/5": {
        "intro": "Nice work! Your submission is very solid.",
        "issues": "Just a few minor issues to address:",
        "outro": "You're doing great, just a little polish and you'll nail it!"
    },
    "3/5": {
        "intro": "Good effort! You've got a solid foundation here.",
        "issues": "There are some issues that need attention:",
        "outro": "Keep refining your skills, you're on the right track!"
    },
    "2/5": {
        "intro": "Thanks for your effort! There are some critical issues to fix.",
        "issues": "The following issues need attention:",
        "outro": "Don't worry, just focus on these points and you'll improve quickly!"
    },
    "1/5": {
        "intro": "Thanks for submitting! The task appears to be spam or significantly off-target.",
        "issues": "The following issues were identified:",
        "outro": "Please review the guidelines carefully and try again!"
    }
}

# SBQ-specific feedback templates
SBQ_FEEDBACK_TEMPLATES = {
    "Not Natural (Reading) - Sounds like reading from text": {
        "message": "This task has been sent back to queue due to naturalness issues. The speech sounds like it's being read from a text rather than natural conversation. For future submissions, please ensure your speech sounds conversational and spontaneous."
    },
    "Not Natural (AI-like) - Contains AI-typical requests/conversations": {
        "message": "This task has been sent back to queue due to naturalness issues. The content contains AI-typical requests (like asking for lists, pros/cons, explanations) that don't represent natural human conversation. Please focus on genuine, spontaneous dialogue."
    },
    "Wrong Location - Video location doesn't match selected category": {
        "message": "This task has been sent back to queue due to location mismatch. The location shown in the video evidence does not match the selected category. Please ensure the video evidence accurately represents the chosen recording location."
    },
    "Inappropriate Content - Contains harmful/offensive/NSFW content": {
        "message": "This task has been sent back to queue due to inappropriate content. The recording contains harmful, offensive, or NSFW material that violates our content guidelines. Please review the content policy before future submissions."
    },
    "Category Confusion - Task fits multiple categories, unclear classification": {
        "message": "This task has been sent back to queue due to category ambiguity. The content could fit multiple categories, making classification unclear. Please ensure future recordings have clear, unambiguous category placement."
    }
}