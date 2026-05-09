
param (
    [string]$filePath
)

$content = Get-Content -Path $filePath -Raw
$encodedContent = [uri]::EscapeDataString($content)

$url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=ur&dt=t&q=$encodedContent"

$response = Invoke-RestMethod -Uri $url
$translatedText = ($response | Out-String) -replace '(?s).*?"(.*?)"(?s).*', '$1'
$translatedText = $translatedText.Split([Environment]::NewLine, [StringSplitOptions]::RemoveEmptyEntries)[0]

$destinationPath = $filePath.Replace("docs", "i18n/ur/docusaurus-plugin-content-docs/current")

$translatedText | Out-File -FilePath $destinationPath -Encoding utf8
