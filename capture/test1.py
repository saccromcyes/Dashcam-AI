import json

with open("data/logs/session_log.json", "r") as f:
    logs = json.load(f)

print("Number of logs:", len(logs))
if logs:
    print(json.dumps(logs[-3:], indent=4))  # show last 3 logs
