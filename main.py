from mcstatus import JavaServer
from datetime import datetime
import time
import requests

TARGET_PLAYERS = [
    "ParrotX2", "Wemmbu", "Vitalasy", "Planetlord", "SpokeIsHere",
    "Mapicc", "ashwagg", "TheRealSquiddo", "JumperWho", "Leowo0k",
    "Derapchu", "Fantst", "roshambogames", "RealReeon", "FlameFrags",
    "Manepear", "Wifies", "PrinceZam", "Peentar", "Rekrap2",
    "ClownPierce", "Kenadian", "eggchan", "4CVIT"
]

SERVER_LIST_FILE = "servers.txt"
LOG_FILE = "players_join.log"

# Put your Discord webhook URL here:
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"

def load_servers(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def send_to_discord(message):
    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"[DISCORD ERROR] Status code {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[DISCORD ERROR] Exception: {e}")

def log_join(server, player):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_line = f"[JOIN] {player} joined server {server} at {timestamp}"
    with open(LOG_FILE, "a") as log:
        log.write(log_line + "\n")
    send_to_discord(log_line)

def check_server(server_address):
    try:
        server = JavaServer.lookup(server_address)
        status = server.status()
        if status.players.sample:
            for player in status.players.sample:
                if player.name.lower() in (name.lower() for name in TARGET_PLAYERS):
                    log_join(server_address, player.name)
    except Exception:
        pass  # ignore errors silently

def main():
    servers = load_servers(SERVER_LIST_FILE)
    for server in servers:
        check_server(server)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
