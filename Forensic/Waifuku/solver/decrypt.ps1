function Decrypt-Text {
    param (
        [string]$EncryptedText,
        [string]$Key
    )

    $KeyBytes = [System.Text.Encoding]::UTF8.GetBytes($Key.PadRight(32).Substring(0, 32))

    $EncryptedData = [Convert]::FromBase64String($EncryptedText)
    $IV = $EncryptedData[0..15]
    $EncryptedBytes = $EncryptedData[16..($EncryptedData.Length - 1)]

    $AES = [System.Security.Cryptography.Aes]::Create()
    $AES.Key = $KeyBytes
    $AES.IV = $IV

    $Decryptor = $AES.CreateDecryptor()

    $DecryptedBytes = $Decryptor.TransformFinalBlock($EncryptedBytes, 0, $EncryptedBytes.Length)
    [System.Text.Encoding]::UTF8.GetString($DecryptedBytes)
}

$Key = "Lirili-Larila_Tung-Tung-Tung-Sahur"
$EncryptedText = "GOYqtDwMKpz5kLzj8Guu0kXQqV9jur0vFpZe0LcOjzDYi3Mv2gERkwk/T/MQIpeN8PizBKkHwy7UQb49tmTW2LL7wZscNHvqQmjAC+At0jo="
$DecryptedText = Decrypt-Text -EncryptedText $EncryptedText -Key $Key
Write-Host "Decrypted Text: $DecryptedText"