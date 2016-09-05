@echo off

if [%1]==[] (
	set /p simulation="Enter Simulation: "
) else (
	set simulation=%1
)

set control="%simulation%\control-file.ctl"
echo Running G-PhoCS on Control file: "%control%"
G-PhoCS-1-2-3 "%simulation%\control-file.ctl"

if %errorlevel% neq 0 goto exit /b %errorlevel%

echo Running Model_Compare on simulation: "%simulation%"
python ..\run_model_compare.py %simulation%

if %errorlevel% neq 0 (
	echo Model_Compare Failed :(
) else (
	echo SUCCESS! 
)

sleep 1