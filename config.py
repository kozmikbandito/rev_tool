# Sabitler ve hazır metinler
FONT = ("Segoe UI", 9)
COLPAD = 6

# Noktalama için hazır hata mesajları
PUNCT_PRESETS = [
    "konuşma sırasında kısa bir duraksama olmadığı için, transcriptte de virgül olmamalıydı.",
    "konuşma sırasında min bir saniyelik bir duraksama olmadığı için, transcriptte de elipsis olmamalıydı.",
    "konuşma sırasında bu sözcükten sonra kısa bir duraksama olduğu için, transcriptte de virgül eklenmeliydi.",
    "konuşma sırasında bu sözcükten sonra min bir saniyelik bir duraksama olduğu için, transcriptte de elipsis eklenmeliydi.",
    "Custom (write below)"
]

# Kelime sorunları için hazır hata mesajları
WORD_PRESETS = [
    "bu sözcük konuşma sırasında söylenmesine rağmen, transcriptte yer almıyor.",
    "bu sözcük konuşma sırasında söylenmemesine rağmen, transcriptte yer alıyor.",
    "Custom (write below)"
]

# Puan tabanlı geri bildirim metinleri
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
        "issues": "The following issues led to sending the task back to queue:",
        "outro": "Don't worry, just focus on these points and you'll improve quickly!"
    }
}