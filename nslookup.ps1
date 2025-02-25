# Archivo de entrada y salida
$inputFile = "SNETBIB77_15.csv"
$outputFile = "output.csv"

# Crear el archivo de salida y agregar el encabezado
"NSLookup Result" | Out-File -FilePath $outputFile

# Leer cada IP del archivo de entrada y ejecutar nslookup
Import-Csv -Path $inputFile | ForEach-Object {
    $ip = $_.IP
    $result = nslookup $ip | Select-String "Name:" | ForEach-Object { $_.Line.Split(" ")[-1] }
    
    # Si no se encuentra el nombre, guardar un mensaje de error
    if (-not $result) {
        $result = "No DNS Resolution"
    }
    
    # Crear una línea de salida con la IP y el resultado
    $outputLine = "$result"
    
    # Agregar la línea al archivo de salida
    Add-Content -Path $outputFile -Value $outputLine
}

Write-Output "Proceso completado. Los resultados se han guardado en $outputFile"