#   Grid Server Using Docker 
## Overview
This Python script('selenium_grid_server.py') automates building, running, and managing multiple Docker containers with SSH access and Selenium servers, using detail.json for configuration. It also opens separate gnome-terminal windows for each Selenium server and handles clean shutdown on interruption.

## Folder's
  | Name                    | Description                                                                                                                                            |
  |:------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------|
  | Dockerfile              | in that we have chrome,firefox,chromedriver,geckodriver,selenium server,selenium,and tools                                                             |
  | selenium_server.json    | It contains detail of containers, SSH details, and commands                                                                                            |
  | selenium_grid_server.py | First it will build Docker image after building the image then it run the container ,then it start ssh in new terminal then it run the selenium server |

## How to run:
 - Automatic Docker Build:
    Builds the Selenium Docker image using a configured command_a.
 - Container Management:
    Removes any pre-existing containers, runs fresh containers based on user-defined ports.
 - SSH Setup:
    Automatically connects to each container via SSH (sshpass), using username/password credentials.
 - Selenium Server Launch:
    Inside each container, launches a Selenium Standalone Server with a specific port.
 - Multiple Terminal Windows:
    Each Selenium server starts in a new gnome-terminal window for easy monitoring.
 - Graceful Shutdown:
    - When the user interrupts (Ctrl+C), the script:
    - Kills all opened gnome-terminal sessions.
    - Stops Selenium servers inside containers.
    - Stops and deletes Docker containers.
    - Cleans up lingering Docker proxy processes.
## Run :
 - First
    - **python3 selenium_grid_server.py**
 - Second
   - To kill pid and remove containers PRESS **Ctrl+c** after running the code


