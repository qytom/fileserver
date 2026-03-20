$repo = "qytom/fileserver"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$downloadPath = Join-Path $desktopPath "FileServer-APK"

Write-Host "=== GitHub Actions APK Downloader ===" -ForegroundColor Green
Write-Host "Repository: $repo" -ForegroundColor Cyan
Write-Host "Download to: $downloadPath" -ForegroundColor Cyan
Write-Host ""

$url = "https://api.github.com/repos/$repo/actions/runs?per_page=1"
$response = Invoke-WebRequest -Uri $url -UseBasicParsing
$data = $response.Content | ConvertFrom-Json
$run = $data.workflow_runs[0]

Write-Host "Latest build:" -ForegroundColor White
Write-Host "  ID: $($run.id)" -ForegroundColor White
Write-Host "  Status: $($run.status)" -ForegroundColor White
Write-Host "  Conclusion: $($run.conclusion)" -ForegroundColor White
Write-Host "  Created: $($run.created_at)" -ForegroundColor White
Write-Host ""

if ($run.status -ne "completed") {
    Write-Host "Build is not completed yet. Please wait..." -ForegroundColor Yellow
    exit 1
}

if ($run.conclusion -ne "success") {
    Write-Host "Build failed. Cannot download APK." -ForegroundColor Red
    exit 1
}

$artifactsUrl = "https://api.github.com/repos/$repo/actions/runs/$($run.id)/artifacts"
$artifactsResponse = Invoke-WebRequest -Uri $artifactsUrl -UseBasicParsing
$artifactsData = $artifactsResponse.Content | ConvertFrom-Json

Write-Host "Artifacts count: $($artifactsData.total_count)" -ForegroundColor White

if ($artifactsData.total_count -eq 0) {
    Write-Host "No artifacts found. Checking build logs..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please visit the build page to check what happened:" -ForegroundColor Cyan
    Write-Host "  $($run.html_url)" -ForegroundColor Cyan
    exit 1
}

if (-not (Test-Path $downloadPath)) {
    New-Item -ItemType Directory -Path $downloadPath | Out-Null
    Write-Host "Created directory: $downloadPath" -ForegroundColor Green
}

foreach ($artifact in $artifactsData.artifacts) {
    Write-Host ""
    Write-Host "Downloading: $($artifact.name)" -ForegroundColor White
    Write-Host "Size: $([math]::Round($artifact.size_in_bytes / 1MB, 2)) MB" -ForegroundColor White
    
    $downloadUrl = $artifact.archive_download_url
    $zipPath = Join-Path $downloadPath "$($artifact.name).zip"
    
    Write-Host "Downloading to: $zipPath" -ForegroundColor White
    
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -UseBasicParsing
        Write-Host "Download completed!" -ForegroundColor Green
        
        Write-Host "Extracting..." -ForegroundColor White
        Expand-Archive -Path $zipPath -DestinationPath $downloadPath -Force
        Write-Host "Extraction completed!" -ForegroundColor Green
        
        Remove-Item $zipPath -Force
        Write-Host "Cleaned up zip file" -ForegroundColor Gray
    }
    catch {
        Write-Host "Download failed: $_" -ForegroundColor Red
        Write-Host "You may need to authenticate with GitHub." -ForegroundColor Yellow
        Write-Host "Please visit: $downloadUrl" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "=== Download completed ===" -ForegroundColor Green
Write-Host "APK files are in: $downloadPath" -ForegroundColor Cyan
Write-Host ""

$apkFiles = Get-ChildItem -Path $downloadPath -Filter "*.apk" -Recurse
if ($apkFiles) {
    Write-Host "Found APK files:" -ForegroundColor White
    $apkFiles | ForEach-Object {
        Write-Host "  $($_.FullName)" -ForegroundColor White
        Write-Host "  Size: $([math]::Round($_.Length / 1MB, 2)) MB" -ForegroundColor Gray
    }
}
