from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from tkinter import filedialog
from difflib import SequenceMatcher
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Ensure you have downloaded necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

def similarity(text1, text2):
    # Calculate similarity ratio between two texts
    return SequenceMatcher(None, text1, text2).ratio()

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    # Convert to lowercase
    tokens = [word.lower() for word in tokens]
    # Remove punctuation
    table = str.maketrans('', '', string.punctuation)
    tokens = [word.translate(table) for word in tokens]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def browse_files():
    global selected_files
    selected_files = filedialog.askopenfilenames(initialdir="/", title="Select Files",
                                                 filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    # Clear the textbox before inserting new files
    textbox.delete("1.0", END)
    # Display the selected file paths in the textbox
    for file in selected_files:
        file_name = file.split('/')[-1]
        textbox.insert(END, file_name + '\n')

def check_plagiarism():
    if not selected_files:
        return

    # Read the content of each selected file
    file_contents = []
    for file in selected_files:
        with open(file, 'r') as f:
            content = f.read()
            preprocessed_content = preprocess_text(content)
            file_contents.append(preprocessed_content)

    # Create a new window to display the results
    result_window = Toplevel(root)
    result_window.title("Plagiarism Check Result")
    result_window.geometry("600x400")
    result_window.resizable(False, False)
    result_window.iconphoto(False, icon_logo)

    result_text = Text(result_window, height=20, width=70)
    result_text.pack()

    # Compare each file with every other file exactly once
    num_files = len(file_contents)
    for i in range(num_files):
        for j in range(i + 1, num_files):
            sim_score = similarity(file_contents[i], file_contents[j])
            similarity_percentage = int(sim_score * 100)
            result_text.insert(END, f"Similarity between {selected_files[i].split('/')[-1]} and {selected_files[j].split('/')[-1]}: {similarity_percentage}%\n")

root = Tk()
root.geometry("800x600")
root.resizable(False, False)
root.title("Plagiarism Checker")
icon_logo = PhotoImage(file="logo.png")
root.iconphoto(False, icon_logo)

# Applying main logo
image_path = "mainlogo.png"  # Replace with the path to your image file
original_image = Image.open(image_path)

# Resize the image to a smaller size
new_width = 100  # Set the width to your desired size
new_height = 100  # Set the height to your desired size
resized_image = original_image.resize((new_width, new_height))
resized_image_tk = ImageTk.PhotoImage(resized_image)
label = Label(root, image=resized_image_tk)
label.place(x=10, y=10)

# Applying title
logoname1 = Label(root, text="Plagiarism ", font=font.Font(size=16, family="Archivo Black"))
logoname1.place(x=120, y=35)

logoname2 = Label(root, text="Checker ", font=font.Font(size=16, family="Archivo Black"))
logoname2.place(x=120, y=60)

# Placing button
check_button = Button(root, text="Check plagiarism", font=font.Font(size=12, family="Archivo Black"),
                      bg="#f4c524", fg="black", height=2, width=14, borderwidth=5, relief="ridge", command=check_plagiarism)
check_button.place(x=600, y=30)

displaytext = Label(root, text="1. Click the 'Browse Files' button to select the text files you want to check for plagiarism.\n"
                               "2. After selecting the files, click the large yellow button labeled 'Check Plagiarism'.\n"
                               "3. Sit back and relax as the tool analyzes the selected files and compares their content.")
displaytext.place(x=150, y=150)


browse_button = Button(root, text="Browse Files", command=browse_files)
browse_button.place(x=350, y=250)

# Create a Text widget to display selected file paths
textbox = Text(root, height=10, width=50)
textbox.place(x=200, y=300)

# Initialize selected_files as an empty list
selected_files = []

root.mainloop()
