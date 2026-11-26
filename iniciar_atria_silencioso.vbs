Set oShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strDir = fso.GetParentFolderName(WScript.ScriptFullName)
exePath = strDir & "\Iniciar_ATRIA.exe"
If fso.FileExists(exePath) Then
    oShell.Run """" & exePath & """", 0, False
Else
    batPath = strDir & "\iniciar_atria.bat"
    oShell.Run """" & batPath & """", 0, False
End If
