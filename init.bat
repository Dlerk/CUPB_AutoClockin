@ECHO off
cd %~dp0
cmd /k "pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"