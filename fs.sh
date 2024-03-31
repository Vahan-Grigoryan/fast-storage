args=("$@")
current_dir=$(pwd)
cd "$(dirname "$0")"
python3 fs.py "${args[@]}"
cd "$current_dir"
