Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell.exe -ExecutionPolicy Bypass -File ""C:\hidden\agent.ps1"" -Verb RunAs", 0, False