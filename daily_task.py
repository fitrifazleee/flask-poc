from datetime import datetime

#buat long entry setiap kali runs os

with open("/home/galactic/script_log.txt", "a") as f:
	f.write(f'Script ran successfully at: {datetime.now()}\n")

print("Task Completed!")
