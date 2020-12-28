mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
python addGA.py
