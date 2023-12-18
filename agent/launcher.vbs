Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File ""agent.ps1"" -Verb RunAs -WindowStyle Hidden", 0, False