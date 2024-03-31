@echo off

set all_args=%*
set current_dir=%cd%
cd %~dp0
py fs.py %all_args%
cd %current_dir%
