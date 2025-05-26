# Step 1: Set your global git config (only once)
git config --global user.name "yourusername"
git config --global user.email "youremail@example.com"
git config --list

# Step 2: Clone the repo into your current directory
git clone https://github.com/ayndvee/CS-2450-Project.git

# Step 3: Change into the project directory
cd CS-2450-Project

# Step 4: Start working — example commands to add, commit, and push changes
git add .
git commit -m "Your message here"
git push

# Optional: Pull latest changes from remote before pushing
git pull