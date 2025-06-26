# CS-2450 Project

## Running the Program
Run the program from the src folder.
The program can be run in two different ways:
1. From the Command Line
2. From a GUI

## 1. Command Line

```
python main.py <filename>
```

or

```
python main.py <filepath>
```

## 2. GUI
```
python main.py
```

Once the GUI is up an running you will then be able to input the file and test it out.


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
```
git config --global user.name "yourusername"
git config --global user.email "youremail@example.com"
git config --list
```
# Step 2: Clone the repo into your current directory
```
git clone https://github.com/ayndvee/CS-2450-Project.git
```

# Step 3: Change into the project directory
```
cd CS-2450-Project
```

# Step 4: Start working — example commands to add, commit, and push changes
```
git add .
git commit -m "Your message here"
git push
```

# Optional: Pull latest changes from remote before pushing
```
git pull
```