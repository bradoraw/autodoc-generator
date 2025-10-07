import subprocess
import yaml
import os

shots_file = "shots.yml"
login_file = "login.yml"
auth_file = "auth.json"

with open(login_file, "r") as f:
    login = yaml.safe_load(f)

print(f"Logging in to {login[0]['url']}")
subprocess.run(["shot-scraper", "auth", login[0]["url"], auth_file])

with open(shots_file, "r") as f:
    shots = yaml.safe_load(f)

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# delete all files in the screenshots directory
for file in os.listdir("screenshots"):
    os.remove(os.path.join("screenshots", file))

print(f"Capturing screenshots for {len(shots)} pages")
for shot in shots:
    url = shot["url"]
    output_file = shot["output"]
    subprocess.run(["shot-scraper", url, "--auth", auth_file, "--wait", "3000", "--output", output_file])