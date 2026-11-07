
#!/data/data/com.termux/files/usr/bin/bash

clear
cd "$(dirname "$0")" || exit 1

echo -e "\033[1;31m"
echo "Starting THE PAIN TDL..."
echo -e "\033[0m"

if ! command -v python >/dev/null 2>&1; then
    echo "Python is not installed."
    echo "Run: pkg install python -y"
    exit 1
fi

if [ ! -f tool.py ] || [ ! -f config.txt ]; then
    echo "Project files are missing!"
    exit 1
fi

python tool.py
