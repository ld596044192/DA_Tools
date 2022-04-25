import win32gui as w

title = w.GetWindowText(w.GetForegroundWindow())

print(title)