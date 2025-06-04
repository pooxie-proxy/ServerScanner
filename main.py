from mcstatus import JavaServer
from datetime import datetime
import time

SERVER_LIST_FILE = "servers.txt"
LOG_FILE = "players_join.log"

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
    print(f"Checking server: {server_address}")
    try:
        server = JavaServer.lookup(server_address)
        status = server.status()
        if status.players.sample:
            for player in status.players.sample:
                print(f"Found player {player.name} on {server_address}")
                log_join(server_address, player.name)
                yield 1
        else:
            print(f"No players online on {server_address}")
    except Exception as e:
        print(f"Failed to query {server_address}: {e}")

def main():
    servers = load_servers(SERVER_LIST_FILE)
    total_joins_logged = 0
    print("Type 'exit' and press Enter to quit.")

    while True:
        joins_this_round = 0
        print(f"\nScanning {len(servers)} servers...")

        for server in servers:
            # check_server yields 1 for each join logged
            for join_event in check_server(server):
                joins_this_round += join_event

            time.sleep(0.5)  # gentle delay

        total_joins_logged += joins_this_round
        print(f"Scanning {len(servers)} servers. {total_joins_logged} join events logged.")

        # Wait for user input with a timeout (non-blocking)
        # If user types 'exit', quit; else continue scanning
        print("Press Enter to scan again or type 'exit' to quit.")
        user_input = input().strip().lower()
        if user_input == "exit":
            print("Exiting. Goodbye!")
            break

if __name__ == "__main__":
    main()
