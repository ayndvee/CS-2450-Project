# CS-2450 Project

## Running the Program

This project uses Python. To run the simulator, use the following command from the src directory:

```
python UVSim.py <filename>
```

or

```
python UVSim.py <filepath>
```

### Example
File in the same directory:
```
python UVSim.py Test1.txt
```

#### File Path Example
Full file path for text file:
```
python UVSim.py /c/Users/name/Documents/Test1.txt
```

Relative path from project root:
```
python ./UVSim-Project/src/UVSim.py Test1.txt
```

Also make sure that the program you want to run is a BasicML program.

# Setting up the Project

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