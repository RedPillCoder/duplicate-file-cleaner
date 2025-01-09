@echo off
setlocal enabledelayedexpansion

:: Set folder path
set "folder=%USERPROFILE%\Downloads"

:: Create temporary files for duplicates
set "tempFile=%TEMP%\file_hashes.txt"
set "deleteList=%TEMP%\delete_list.txt"
if exist "%tempFile%" del "%tempFile%"
if exist "%deleteList%" del "%deleteList%"

:: Generate hashes for all files in the folder
for /r "%folder%" %%f in (*) do (
    for /f "delims=" %%h in ('certutil -hashfile "%%f" MD5 ^| findstr /v /c:"MD5 hash" /c:"CertUtil"') do (
        echo %%h "%%~f" >> "%tempFile%"
    )
)

:: Identify duplicates
set "lastHash="
set "lastFile="
for /f "tokens=1,* delims= " %%a in ('sort "%tempFile%"') do (
    if "!lastHash!"=="%%a" (
        if defined lastFile (
            echo !lastFile! >> "%deleteList%"
        )
        set "lastFile=%%b"
    ) else (
        set "lastHash=%%a"
        set "lastFile=%%b"
    )
)

:: Check if duplicates exist
if not exist "%deleteList%" (
    echo No duplicate files found.
    goto cleanup
)

:: Display duplicates
echo The following duplicate files will be deleted:
for /f "delims=" %%f in (%deleteList%) do (
    echo %%~f
)
echo.

:: Confirm deletion
choice /m "Do you want to proceed with deleting these files?"
if errorlevel 2 (
    echo Operation canceled.
    goto cleanup
)

:: Delete duplicates with debugging output
echo Deleting files...
for /f "delims=" %%f in (%deleteList%) do (
    set "filePath=%%~f"
    
    echo Attempting to delete: !filePath!
    
    if exist "!filePath!" (
        takeown /F "!filePath!" >nul 2>&1
        icacls "!filePath!" /grant %username%:F >nul 2>&1
        
        :: Debugging output for self-deletion check
        echo Current script path: %~f0
        echo Comparing: !filePath! with %~f0

        :: Check if the current script is trying to delete itself
        if /I "!filePath!" NEQ "%~f0" (
            del /F /Q "!filePath!"
            if errorlevel 1 (
                echo Failed to delete: !filePath!
            ) else (
                echo Successfully deleted: !filePath!
            )
        ) else (
            echo Skipped self-deletion of the script file: !filePath!
        )
    ) else (
        echo File not found: !filePath! (skipped)
    )
)
pause

:: Cleanup temporary files
:cleanup
if exist "%tempFile%" del "%tempFile%"
if exist "%deleteList%" del "%deleteList%"
endlocal
echo Done.
