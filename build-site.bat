pyinstaller  -Fw  ^
    --workpath ./build/ ^
    --distpath ./dist/ ^
    -n site_dev_temp app.py  --clean --noconfirm

