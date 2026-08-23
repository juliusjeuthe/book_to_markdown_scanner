param(
  [string]$RepoPath = "."
)

$repo = Resolve-Path $RepoPath
Set-Location $repo

# Try to run git gui
try {
    git gui
    exit 0
} catch {
    # try common Git for Windows locations
    $possible = @(
        "${env:ProgramFiles}\Git\cmd\git-gui.exe",
        "${env:ProgramFiles}\Git\mingw64\bin\git-gui.exe",
        "${env:ProgramFiles(x86)}\Git\cmd\git-gui.exe"
    )
    foreach ($p in $possible) {
        if (Test-Path $p) {
            & $p
            exit 0
        }
    }
    Write-Error "Could not launch 'git gui'. Ensure Git for Windows is installed (https://git-scm.com/download/win) and 'git gui' is on PATH."
    exit 1
}
