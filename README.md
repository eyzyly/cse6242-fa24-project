# CSE6242 - Data & Visual Analytics - Fall 2024

## Prerequisites

Before you begin, ensure you have the following software installed:

1. **Visual Studio Code** - Download and install from [Visual Studio Code](https://code.visualstudio.com/).
2. **Dev Containers Extension** - Install the Dev Containers extension from the VS Code Marketplace.
3. **Docker Desktop** - Download and install from [Docker Desktop](https://www.docker.com/products/docker-desktop).
4. **GitHub Account** - Set up a GitHub account if you don’t already have one.

## Setting Up Your Development Environment

1. **Fork the Project Repository**  
   Fork the project repo by visiting [this link](https://github.com/eyzyly/cse6242-fa24-project).

2. **Find Your Home Directory**  
   Use the following command based on your operating system to find your home directory:
   - **Windows (PowerShell):**
     ```powershell
     $HOME
     ```
   - **Linux/MacOS (Terminal):**
     ```bash
     echo $HOME
     ```

3. **Create the `.dbt` Folder**  
   Navigate to your home directory and create a folder called `.dbt`:
   ```bash
   mkdir $HOME/.dbt
   ```

4. **Create the `profiles.yml` File**  
   In the `.dbt` folder, create an empty file named `profiles.yml`:
   ```bash
   touch $HOME/.dbt/profiles.yml
   ```

5. **Add Boilerplate Code to `profiles.yml`**  
   Open the `profiles.yml` file and paste the following boilerplate code:
   ```yaml
   cse6242_dbt:
     target: personal
     outputs:
       personal:
         dataset: dbt_<ez> # replace <ez> with your initials, e.g., dbt_ez, dbt_bf, etc.
         job_execution_timeout_seconds: 300
         job_retries: 1
         location: US
         method: oauth
         priority: interactive
         project: <GCP project id> # find from Notion
         threads: 10
         type: bigquery
         
        production:
         dataset: analytics 
         job_execution_timeout_seconds: 300
         job_retries: 1
         location: US
         method: oauth
         priority: interactive
         project: <GCP project id> # find from Notion
         threads: 10
         type: bigquery
   ```

6. **Open the Project in VS Code**  
   Open Visual Studio Code and navigate to the project directory:
   ```bash
   cd cse6242-fa24-project
   ```

7. **Rebuild the Dev Container**  
   In VS Code, look for the green square with two chevrons (>) at the bottom left. Click on it and select the option to rebuild the container using `ingestion_transform`.

8. **Wait for Installation**  
   Wait for the installation to complete. This may take a few minutes, and you should see a message saying "Done, press any key to go to the terminal."

9. **Restart VS Code**  
   Although it may seem strange, close the VS Code window and open it again.

10. **Reopen the Project in the Container**  
    Go to the project directory again. A "Reopen in Container" prompt should appear. Click it!

11. **Verify the Dev Container Configuration**  
    Once the container is reopened, it should be configured correctly for development.