pyinstaller  -Fw  ^
    --workpath ./build/ ^
    --distpath ./dist/ ^
    -n fastapi_dev_temp main.py  --clean --noconfirm

