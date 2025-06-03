@echo off
REM -------------------------------------------------------
REM  Change working directory to the script’s own folder
REM -------------------------------------------------------
cd /d "%~dp0"

REM -------------------------------------------------------
REM  Loop over each Python file beginning with "vfs_"
REM  but skip "vfs_main.py"
REM -------------------------------------------------------
for %%f in (vfs_*.py) do (
    if /I "%%~nxf"=="vfs_main.py" (
        echo Skipping %%f...
    ) else (
        echo Launching %%f…
        start cmd /k python %%~f
	timeout /t 40 /nobreak >nul
    )
)

REM -------------------------------------------------------
REM  Keep this controller window open to see any messages
REM -------------------------------------------------------
pause