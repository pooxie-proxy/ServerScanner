from mcstatus import JavaServer
from datetime import datetime
import time

SERVER_LIST_FILE = "servers.txt"
LOG_FILE = "players_join.log"

def load_servers(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def log_join(server, player):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_line = f"[JOIN] {player} joined server {server} at {timestamp}"
    with open(LOG_FILE, "a") as log:
        log.write(log_line + "\n")

def check_server(server_address):
    try:
        server = JavaServer.lookup(server_address)
        status = server.status()
        if status.players.sample:
            for player in status.players.sample:
                log_join(server_address, player.name)
    except Exception:
        pass  # ignore any errors silently

def main():
    servers = load_servers(SERVER_LIST_FILE)
    print(f"Scanning {len(servers)} servers...")
    for i, server in enumerate(servers, 1):
        check_server(server)
        if i % 10 == 0:
            print(f"Scanned {i} servers...")
        time.sleep(0.5)  # gentle delay to avoid spamming

if __name__ == "__main__":
    main()
