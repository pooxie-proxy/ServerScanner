import threading
from mcstatus import JavaServer
from datetime import datetime
import time
import sys

SERVER_LIST_FILE = "servers.txt"
LOG_FILE = "players_join.log"

stop_flag = False

def load_servers(filename):
    with open(filename, "r") as f:
        servers = [line.strip() for line in f if line.strip()]
    print(f"Loaded {len(servers)} servers: {servers}")
    return servers

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
                yield 1
    except Exception:
        pass

def input_listener():
    global stop_flag
    while True:
        cmd = input()
        if cmd.strip().lower() == "exit":
            print("Exit command received. Stopping scan...")
            stop_flag = True
            break

def main():
    global stop_flag
    servers = load_servers(SERVER_LIST_FILE)
    total_joins_logged = 0

    # Start input listener thread
    listener_thread = threading.Thread(target=input_listener, daemon=True)
    listener_thread.start()

    print("Starting continuous scan. Type 'exit' and press Enter to stop.")

    while not stop_flag:
        joins_this_round = 0

        for server in servers:
            if stop_flag:
                break
            for join_event in check_server(server):
                joins_this_round += join_event
            time.sleep(0.5)  # gentle delay between servers

        total_joins_logged += joins_this_round
        print(f"Scanned {len(servers)} servers. Total join events logged: {total_joins_logged}")

    print("Scan stopped.")

if __name__ == "__main__":
    main()
