import subprocess
import json
import time
import os
import sys

# Load login details from 'detail.json'
with open("selenium_server_details.json", "r") as f:
    login = json.load(f)

# Docker commands
command_a = login['command_a']
command_b_template = login['command_b']

# Containers list
containers = login['containers']

# Track gnome-terminal processes
terminal_processes = []
container_processes = []

# Function to remove existing container
def remove_existing_container(container_name):
    print(f"Checking if container {container_name} exists...")
    subprocess.run(f"docker rm -f {container_name}", shell=True, capture_output=True, text=True)

# Build and run a container
def build_and_run_container(container):
    print(f"\nBuilding and running container: {container['name']}")

    remove_existing_container(container['name'])

    image_build = subprocess.run(command_a, shell=True, capture_output=True, text=True)
    if image_build.returncode == 0:
        print(f"Image built successfully for {container['name']}")
    else:
        print(f"Build error for {container['name']}:\n{image_build.stderr}")

    run_command = command_b_template.format(
        container_name=container['name'],
        ssh_port=container['ssh_port'],
        selenium_port=container['selenium_port']
    )
    image_run = subprocess.run(run_command, shell=True, capture_output=True, text=True)
    if image_run.returncode == 0:
        print(f"Container {container['name']} started.")
    else:
        print(f"Run error for {container['name']}:\n{image_run.stderr}")

    time.sleep(3)

    subprocess.run(
        f"docker exec {container['name']} sudo service ssh start",
        shell=True,
        capture_output=True,
        text=True
    )
    print(f"SSH service started in {container['name']}.")

# Prepare SSH + Java commands for each container
def prepare_ssh_commands():
    ssh_commands = []

    ssh_username = login['ssh']['username']
    ssh_password = login['ssh']['password']
    ssh_host = login['ssh']['hostname']

    for container in containers:
        ssh_port = container['ssh_port']
        java_command = login['java_command_template'].format(
            selenium_port=container['selenium_port']
        )

        full_command = (
            f"sshpass -p {ssh_password} ssh -o StrictHostKeyChecking=no "
            f"{ssh_username}@{ssh_host} -p {ssh_port} '{java_command}'"
        )

        ssh_commands.append(full_command)

    return ssh_commands

# Open new gnome-terminals for each command
def open_new_terminals(commands):
    global terminal_processes

    for cmd in commands:
        print(f"Opening new terminal with command: {cmd}")
        process = subprocess.Popen(
            f'gnome-terminal -- bash -c "{cmd}; exec bash"',
            shell=True
        )
        terminal_processes.append(process)
        print(f"Started terminal for command with PID {process.pid}")
# Kill all gnome-terminal processes and stop selenium server inside containers
def kill_all_terminals():
    print("\nKilling all gnome-terminal processes...")

    # Iterate through all terminal processes and kill them
    for process in terminal_processes:
        try:
            print(f"Terminating process with PID {process.pid}...")
            process.terminate()  # Try to gracefully terminate
            process.wait(timeout=5)  # Wait for graceful shutdown
            print(f"Terminated process with PID {process.pid}")
        except subprocess.TimeoutExpired:
            print(f"Force killing process PID {process.pid}")
            process.kill()

    # After attempting to kill, ensure no remaining processes
    print("\nEnsuring all terminal processes are killed.")
    for process in terminal_processes:
        if process.poll() is None:  # Check if process is still running
            print(f"Force killing remaining process PID {process.pid}")
            process.kill()

    # Stop Selenium servers and remove containers
    for container in containers:
        print(f"\nStopping Selenium server in {container['name']}...")
        subprocess.run(
            f"docker exec {container['name']} pkill -f 'java -jar selenium-server.jar'",
            shell=True,
            capture_output=True,
            text=True
        )
        print(f"Selenium server stopped in {container['name']}.")

        # Stop and remove containers
        print(f"Stopping container {container['name']}...")
        subprocess.run(
            f"docker stop {container['name']}",
            shell=True,
            capture_output=True,
            text=True
        )
        print(f"Container {container['name']} stopped.")

        print(f"Removing container {container['name']}...")
        subprocess.run(
            f"docker rm -f {container['name']}",
            shell=True,
            capture_output=True,
            text=True
        )
        print(f"Container {container['name']} removed.")

    # Kill lingering docker-pr processes using sudo
    print("\nKilling any lingering docker-pr processes...")
    subprocess.run("sudo pkill -f docker-pr", shell=True)

# Main function
def main():
    try:
        # Build and run all containers
        for container in containers:
            build_and_run_container(container)

        # Wait for containers to stabilize
        time.sleep(3)

        # Prepare SSH commands for each container
        ssh_commands = prepare_ssh_commands()

        # Open a new terminal for each container
        open_new_terminals(ssh_commands)

        # Keep script alive until interrupted
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        kill_all_terminals()

if __name__ == "__main__":
    main()

