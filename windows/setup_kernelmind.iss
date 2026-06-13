[Setup]
AppName=KernelMind
AppVersion=1.0.0
DefaultDirName={pf}\KernelMind
DefaultGroupName=KernelMind
UninstallDisplayIcon={app}\KernelMind.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=KernelMind_Setup

[Files]
Source: "dist\KernelMind.exe"; DestDir: "{app}"
Source: "kernelmind.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\KernelMind"; Filename: "{app}\KernelMind.exe"
Name: "{group}\Desinstalar"; Filename: "{uninstallexe}"
Name: "{commondesktop}\KernelMind"; Filename: "{app}\KernelMind.exe"

[Run]
Filename: "{app}\KernelMind.exe"; Description: "Iniciar KernelMind"; Flags: postinstall nowait skipifsilent
