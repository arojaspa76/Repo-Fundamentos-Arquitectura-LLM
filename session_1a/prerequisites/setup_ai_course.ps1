# Create directory structure for AI Python course

$root = "AI-Python-Course"
$folders = @("notebooks", "data", "src", "results")

if (!(Test-Path -Path $root)) {
    New-Item -ItemType Directory -Path $root
}

foreach ($folder in $folders) {
    $path = Join-Path -Path $root -ChildPath $folder
    if (!(Test-Path -Path $path)) {
        New-Item -ItemType Directory -Path $path
    }
}

New-Item -Path "$root\README.md" -ItemType File -Force
New-Item -Path "$root\requirements.txt" -ItemType File -Force
New-Item -Path "$root\Makefile" -ItemType File -Force

Write-Output "Directory structure created successfully!"
