# no-lallygagging
So the lally of the valley (you know who you are) can hopefully lock in a little better :D
If you're not the lally of the valley (how did you get here then) feel free to use it still

## Disclaimer
I used ChatGPT for a lot of this since it's like a one-off project that I don't need to know that well.  So if you go digging through the code you'll see some weird stuff and I just wanted to say, that ain't me that put them there


# Installing Python
## Windows

1. Go to the official Python downloads page:
   - https://www.python.org/downloads/

2. Download the latest stable version for Windows.

3. Run the installer.

4. **Important:** Check the box:
   - **Add Python to PATH**

5. Click **Install Now** and complete the installation.

6. Verify the installation:
   - Open **Command Prompt**.
   - Run:
     ```bash
     python --version
     ```
     or:
     ```bash
     py --version
     ```

7. Test Python:
   ```bash
   python
   ```

   Then enter:

   ```python
   print("Hello, world!")
   ```

   Exit Python:

   ```python
   exit()
   ```

---

## macOS
### Option 1: Install from Python.org

1. Go to:
   - https://www.python.org/downloads/macos/

2. Download the latest macOS installer.

3. Open the `.pkg` file and follow the installation wizard.

4. Verify the installation:

   ```bash
   python3 --version
   ```

5. Start Python:

   ```bash
   python3
   ```
---

## Troubleshooting

### Windows: "python is not recognized"

Reinstall Python and ensure **Add Python to PATH** is checked during installation.

### macOS: `python` not found but `python3` works

This is normal on many macOS versions. Use:

```bash
python3
pip3
```

### Permission errors when installing packages

Use a virtual environment instead of installing packages globally.

```bash
python -m venv .venv
```

Then activate it and install packages with `pip`.

---

# Getting the Files onto Your Computer
If you're reading this then you're right where you need to be.

1. Find the green button that says "Code" and click it
2. Press on "Download Zip"
3. Extract the zip file to the folder/location of your choice

---

# Running the Program
1. Navigate to the folder where you placed the unzipped items
    - You should be looking at a bunch of the folders like "bible" and "core" and a file called "main.py"
2. Right click on any empty section and hit "Open in Terminal" or "Open in Command Line" or anything along those lines
    - You can also click into the address bar, type ```cmd``` and hit enter
3. Once in the command line type in ```python3 main.py``` and hit enter and the program should run

---

# Program Features
## The Bible
1. Clicking on "Bible" brings you to the Bible reader
    - It's from my own custom Bible reader and it's here because I needed to reuse some of the code
    - It's functional but a little janky compared to my own version
2. The start reading just select the desired Version, Book, and Chapter from the dropdowns
    - The .usfx file is CUV in traditional (sorry lally of the valley)
    - I'm technically not allowed to share some versions with you so just be cool and don't get me in trouble alright?

## Quiz Creator
This is what I really made this for
1. Clicking on Quiz brings you to the Quiz page

2. Select your Version
    - Don't pick CUV as it won't generate the quiz properly as all the quiz features are setup for English versions - again, code was reused which is why the CUV versison appears

3. Select your Book and Chapter next

4. Put in the verses you want to be tested on in the Verse section

5. Select your difficulty for the blanks in the verses
    - The way the blanks work is that it will generate blanks for words that are not on the skip list
        - The skip list can be edited under "quiz_utils.py" for if you want to add or remove some words
    - Currently the values are set at "Wittle Baby": 10, "Easy": 25, "Medium": 50, "Hard": 75, "All": 100
        - This means that if you set difficulty to "Wittle Baby" then only 10% of the non-skipped words will be blanked - "All" will blank out 100% of the words
    - You can change the values yourself if you want by going to the get_difficulty_percent function in "quiz_screen.py"
6. Hit "Generate Quiz"
    - When you're done with the quiz you don't have to hit "Clear" then "Generate Quiz" if you want to make a new one, you can just hit "Generate Quiz"

7. Fill in the blanks however you want

8. To see answers there are multiple options
    - You can click on the blanks to show the answers for that blank
    - You can click on reveal random to reveal a random word from all the blanks
    - Reveal all is pretty self-explanatory

### Other features
- Clear is used for when there is a test created and it just brings back the verses
- The Text Size slider on the top right is there because I don't know the size of your screens and auto-wrapping the text was a headache so I just said screw it and went with the brute force option

---

# Current Issues
Feel free to tell me what other issues you see since you know how to reach me anyways

1. If the Quiz is long enough that you have the scroll, clicking a blank will reset you to the top of the page, meaning you will have to keep scrolling down again to get to where you were

2. The aforementioned issue of no Chinese fill-in-the-blank but I'm sure that's not an issue to you, lally