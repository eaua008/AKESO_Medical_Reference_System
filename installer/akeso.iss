; =====================================================================
; Akeso installer (Inno Setup 6)
; ---------------------------------------------------------------------
; Turns dist\Akeso (the PyInstaller build) into ONE file:
;     installer\Output\Akeso-Setup-1.0.0.exe
; Testers double-click it like any installer: it copies Akeso to their
; computer, adds Start menu (and optional desktop) shortcuts, and appears
; in Settings > Apps so it can be uninstalled normally.
;
; Build order (from the project folder, in IntelliJ's Terminal):
;   1. pyinstaller akeso.spec --noconfirm
;   2. & "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe" installer\akeso.iss
;      (or, if Inno Setup was installed for all users:
;       & "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\akeso.iss)
;
; Installs for the current user only (no administrator prompt), into
; %LOCALAPPDATA%\Programs\Akeso. The user's notes, caches and settings live
; in %LOCALAPPDATA%\Akeso and are NOT removed by uninstalling.
; =====================================================================

#define AppName      "Akeso"
#define AppVersion   "1.0.1"
#define AppPublisher "Eijkim Maulit, Mapua Malayan Colleges Mindanao"
#define AppExe       "Akeso.exe"

[Setup]
; Never change AppId: Windows uses it to recognise updates of the same app.
AppId={{7E69804C-C8DD-4540-8146-B9F61DFE9F2D}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=Output
OutputBaseFilename=Akeso-Setup-{#AppVersion}
SetupIconFile=..\assets\akeso.ico
UninstallDisplayIcon={app}\{#AppExe}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
InfoBeforeFile=..\THIRD_PARTY_NOTICES.md
CloseApplications=yes

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"

[Files]
; Everything PyInstaller built (Akeso.exe + _internal\).
Source: "..\dist\Akeso\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "Open {#AppName} now"; Flags: nowait postinstall skipifsilent
; In-app update (Settings > Updates runs this installer with /VERYSILENT
; /UPDATE): no wizard, so open Akeso again by ourselves when done.
Filename: "{app}\{#AppExe}"; Flags: nowait; Check: IsInAppUpdate

[Code]
// True when started by Akeso's own updater (it passes /UPDATE).
function IsInAppUpdate: Boolean;
var
  i: Integer;
begin
  Result := False;
  for i := 1 to ParamCount do
    if CompareText(ParamStr(i), '/UPDATE') = 0 then
      Result := True;
end;
