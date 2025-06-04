from mcstatus import JavaServer
from datetime import datetime
import time
import requests

# List of target players to track (case-insensitive)
TARGET_PLAYERS = [
    "ParrotX2", "Wemmbu", "Vitalasy", "Planetlord", "SpokeIsHere",
    "Mapicc", "ashwagg", "TheRealSquiddo", "JumperWho", "Leowo0k",
    "Derapchu", "Fantst", "roshambogames", "RealReeon", "FlameFrags",
    "Manepear", "Wifies", "PrinceZam", "Peentar", "Rekrap2",
    "ClownPierce", "Kenadian", "eggchan", "4CVIT"
]

SERVER_LIST_FILE = "servers.txt"
LOG_FILE = "players_seen.log"

# Your Discord webhook URL here
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_id/your_webhook_token"

def load_servers(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def send_to_discord(message):
    data = {
        "content": message
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"[DISCORD ERROR] Status code {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[DISCORD ERROR] Exception: {e}")

def log_sighting(server, player):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_line = f"[JOIN] {player} joined server {server} at {timestamp}"
    with open(LOG_FILE, "a") as log:
        log.write(log_line + "\n")
    print(log_line)
    send_to_discord(log_line)

def check_server(server_address):
    try:
        server = JavaServer.lookup(server_address)
        status = server.status()
        if status.players.sample:
            for player in status.players.sample:
                if player.name.lower() in (name.lower() for name in TARGET_PLAYERS):
                    log_sighting(server_address, player.name)
        else:
            print(f"[CHECKED] {server_address}: No player sample available.")
    except Exception as e:
        print(f"[ERROR] {server_address}: {e}")

def main():
    servers = load_servers(SERVER_LIST_FILE)
    print(f"Scanning {len(servers)} servers for target players...\n")
    for server in servers:
        check_server(server)
        time.sleep(0.5)  # avoid hammering servers

if __name__ == "__main__":
    main()
