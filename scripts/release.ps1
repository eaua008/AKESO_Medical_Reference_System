# =====================================================================
# Release a new Akeso version, start to finish:
#
#   .\scripts\release.ps1 1.0.1 -Notes "In-app updates, announcements, suspension pop-up"
#
#   1. checks everything it needs is there (before changing anything),
#   2. sets the version (app\core\device_identity.py, installer\akeso.iss),
#   3. builds the app (PyInstaller) and the installer (Inno Setup),
#   4. writes the installer's SHA-256 fingerprint,
#   5. publishes both files as a GitHub release on eaua008/akeso-releases
#      (every installed Akeso then shows the green "Update" button),
#   6. commits, tags and pushes the code to your own repository.
#
# Options:
#   -SkipPublish   build only (no GitHub release, no push)
#   -SkipPush      publish the release but do not commit / push the code
#
# Needs once: GitHub CLI.  winget install GitHub.cli   then   gh auth login
# =====================================================================

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidatePattern('^\d+\.\d+\.\d+$')]
    [string]$Version,
    [string]$Notes = "",
    [switch]$SkipPublish,
    [switch]$SkipPush
)

$ErrorActionPreference = "Stop"
$ReleasesRepo = "eaua008/akeso-releases"
$Tag = "v$Version"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Step($text) { Write-Host ""; Write-Host "== $text" -ForegroundColor Cyan }
function Fail($text) { Write-Host ""; Write-Host "STOPPED: $text" -ForegroundColor Red; exit 1 }

# Runs a command quietly; $true if it succeeded. (Windows PowerShell 5.1
# turns a native program's error output into an exception when redirected,
# so errors are relaxed just for this.)
function Test-Ok([scriptblock]$Command) {
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try { & $Command *> $null; return ($LASTEXITCODE -eq 0) }
    catch { return $false }
    finally { $ErrorActionPreference = $previous }
}

function Set-InFile($path, $pattern, $replacement) {
    $full = Join-Path $root $path
    $text = [IO.File]::ReadAllText($full)
    if (-not [Regex]::IsMatch($text, $pattern)) { Fail "No version line found in $path" }
    [IO.File]::WriteAllText($full, [Regex]::Replace($text, $pattern, $replacement), $utf8)
}

# ------------------------------------------------------------- 1. checks
Step "Checking tools"
$python = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) { Fail ".venv not found. Create it and install requirements first." }
if (-not (Test-Ok { & $python -m PyInstaller --version })) {
    Fail "PyInstaller is not installed in .venv. Run: .\.venv\Scripts\pip install pyinstaller"
}
$iscc = @("$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
          "C:\Program Files (x86)\Inno Setup 6\ISCC.exe") |
        Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $iscc) { Fail "Inno Setup 6 (ISCC.exe) not found." }
if (-not (Test-Path ".env")) { Fail ".env is missing: the build would not reach Supabase." }

if (-not $SkipPublish) {
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Fail "GitHub CLI not found. Run: winget install GitHub.cli  (then reopen the terminal and run: gh auth login)"
    }
    if (-not (Test-Ok { gh auth status })) { Fail "GitHub CLI is not signed in. Run: gh auth login" }
    if (Test-Ok { gh release view $Tag --repo $ReleasesRepo }) {
        Fail "Release $Tag already exists on $ReleasesRepo. Use a new version number."
    }
    if (-not $SkipPush) {
        if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail "git not found." }
        if (Test-Ok { git rev-parse -q --verify "refs/tags/$Tag" }) {
            Fail "Your code repository already has a tag $Tag. Use a new version number."
        }
        $tracked = git ls-files -- .env client_secret*.json akeso_session.bin
        if ($tracked) { Fail "Secret files are tracked by git: $tracked. Remove them from git first (git rm --cached)." }
    }
    if (-not $Notes) { $Notes = Read-Host "What changed in $Version? (one line, shown in the app)" }
    if (-not $Notes) { $Notes = "Akeso $Version" }
}
Write-Host "   all good"

# ------------------------------------------------------- 2-4. build
Step "Setting version $Version"
Set-InFile "app\core\device_identity.py" 'APP_VERSION = "[^"]*"' "APP_VERSION = `"$Version`""
Set-InFile "installer\akeso.iss" '#define AppVersion\s+"[^"]*"' "#define AppVersion   `"$Version`""

Step "Building the app (PyInstaller, a few minutes)"
& $python -m PyInstaller akeso.spec --noconfirm
if ($LASTEXITCODE -ne 0) { Fail "PyInstaller failed (see the messages above)." }

Step "Building the installer (Inno Setup)"
& $iscc "installer\akeso.iss"
if ($LASTEXITCODE -ne 0) { Fail "Inno Setup failed (see the messages above)." }

$setup = Join-Path $root "installer\Output\Akeso-Setup-$Version.exe"
if (-not (Test-Path $setup)) { Fail "Installer not found at $setup" }
$hash = (Get-FileHash $setup -Algorithm SHA256).Hash.ToLower()
[IO.File]::WriteAllText("$setup.sha256", "$hash  Akeso-Setup-$Version.exe`n", $utf8)
$size = [Math]::Round((Get-Item $setup).Length / 1MB)
Write-Host "   Akeso-Setup-$Version.exe  ($size MB)" -ForegroundColor Green
Write-Host "   SHA-256 $hash"

if ($SkipPublish) {
    Write-Host ""
    Write-Host "Built only (-SkipPublish). Installer: installer\Output\Akeso-Setup-$Version.exe" -ForegroundColor Green
    exit 0
}

# --------------------------------------------------- 5. GitHub release
Step "Publishing release $Tag on $ReleasesRepo"
if (-not (Test-Ok { gh repo view $ReleasesRepo })) {
    Write-Host "   $ReleasesRepo does not exist yet: creating it (public, installers only)"
    gh repo create $ReleasesRepo --public --add-readme --description "Akeso installers. Source code is not here."
    if ($LASTEXITCODE -ne 0) { Fail "Could not create $ReleasesRepo." }
}
gh release create $Tag $setup "$setup.sha256" --repo $ReleasesRepo --title "Akeso $Version" --notes $Notes --latest
if ($LASTEXITCODE -ne 0) { Fail "Publishing the release failed. Nothing was pushed; run the script again when fixed." }
Write-Host "   https://github.com/$ReleasesRepo/releases/tag/$Tag" -ForegroundColor Green

if ($SkipPush) {
    Write-Host ""
    Write-Host "Released (code not pushed: -SkipPush)." -ForegroundColor Green
    exit 0
}

# ------------------------------------------------------ 6. push the code
Step "Committing and pushing the code"
git add -A
$staged = git diff --cached --name-only
$secret = $staged | Where-Object { $_ -match '(^|/)\.env$|client_secret.*\.json$|akeso_session\.bin$' }
if ($secret) {
    git reset -q
    Fail "Refusing to commit secret files: $secret. Check .gitignore. (The release itself is already published.)"
}
if ($staged) {
    Write-Host "   Files in this commit:"
    $staged | ForEach-Object { Write-Host "     $_" }
    git commit -q -m "Release $Version" -m $Notes
    if ($LASTEXITCODE -ne 0) { Fail "git commit failed." }
} else {
    Write-Host "   nothing new to commit"
}
git tag -a $Tag -m "Akeso $Version"
git push
if ($LASTEXITCODE -ne 0) { Fail "git push failed (the release is published; push again with: git push; git push origin $Tag)" }
git push origin $Tag
if ($LASTEXITCODE -ne 0) { Fail "Pushing the tag failed. Run: git push origin $Tag" }

Write-Host ""
Write-Host "== Akeso $Version is out" -ForegroundColor Green
Write-Host "   Release:  https://github.com/$ReleasesRepo/releases/tag/$Tag"
Write-Host "   Installed copies (1.0.1 and later) show the green Update button within a few hours,"
Write-Host "   or straight away with Settings > Updates > Check for updates."
