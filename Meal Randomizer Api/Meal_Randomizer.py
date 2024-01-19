# "Meal Maker APi"

# Importing necessary modules for the Meal Maker API
import tkinter as tk  # Tkinter is used for creating the GUI
from tkinter import ttk  # ttk provides access to the Tk themed widget set
import requests  # Requests is used for making HTTP requests to The Meal DB API
from PIL import ImageTk, Image  # Pillow  is used for handling images
from io import BytesIO  # BytesIO is used to work with image data in memory
import webbrowser  # Webbrowser is used for opening links in the default web browser


def display_meal_details(meal):
    # Function to display detailed information about a meal

    meal_name = meal["strMeal"]

    # Enabling Text widget for editing
    meal_text.config(state=tk.NORMAL)

    # Clearing existing content
    meal_text.delete("1.0", tk.END)

    # Displaying basic meal information
    meal_text.insert(tk.END, f"Name: {meal_name}\n\n", "center")

    meal_place = meal["strArea"]
    meal_text.insert(tk.END, f"Origin: {meal_place}\n\n", "center")

    meal_class = meal["strCategory"]
    meal_text.insert(tk.END, f"Category: {meal_class}\n\n", "center")

    # Extracting ingredients and measurements
    ingredients = [meal.get(f"strIngredient{i}", "") for i in range(1, 21)]
    measurements = [meal.get(f"strMeasure{i}", "") for i in range(1, 21)]

    # Displaying ingredients and measurements
    meal_text.insert(tk.END, f"Ingredients: {', '.join(filter(None, ingredients))}\n\n", "center")
    meal_text.insert(tk.END, f"Measurements: {', '.join(filter(None, measurements))}\n\n", "center")

    youtube_link = meal["strYoutube"]
    meal_text.insert(tk.END, "YouTube: \n", "center")
    meal_text.insert(tk.END, youtube_link, "youtube_link")
    meal_text.insert(tk.END, "\n\n", "center")

    # Making YouTube link clickable
    meal_text.tag_configure("youtube_link", foreground="blue", underline=True, justify="center")
    meal_text.tag_bind("youtube_link", "<ButtonRelease-1>", lambda e: open_link(youtube_link))

    # Displaying dish image
    dish_image_url = meal["strMealThumb"]
    dish_image_response = requests.get(dish_image_url)

    if dish_image_response.status_code == 200:
        dish_image = Image.open(BytesIO(dish_image_response.content))
        img_width, img_height = dish_image.size
        dish_image = dish_image.resize((200, int(200 * (img_height / img_width))), resample=Image.LANCZOS)
        dish_image = ImageTk.PhotoImage(dish_image)

        dish_image_label.config(image=dish_image, bg="#F9EDCC", bd=2, relief="solid")
        dish_image_label.image = dish_image
    else:
        # Display a placeholder image if the dish image is not available
        placeholder_image = Image.new("RGB", (200, 200), color="#F9EDCC")
        placeholder_image = ImageTk.PhotoImage(placeholder_image)

        dish_image_label.config(image=placeholder_image, bg="#F9EDCC", bd=2, relief="solid")
        dish_image_label.image = placeholder_image

    # Disable Text widget for editing
    meal_text.config(state=tk.DISABLED)

# Function to handle clicks on the YouTube link in the displayed meal details
def on_click(event):
    # Get the current index of the cursor in the meal_text Text widget
    index = meal_text.index(tk.CURRENT)

    # Search for the position of "YouTube:" in the text
    youtube_link_start = meal_text.search("YouTube:", index, tk.END)

    # Check if "YouTube:" is found in the text
    if youtube_link_start:
        # Move to the actual start of the YouTube link
        youtube_link_start = youtube_link_start + len("YouTube:")

        # Search for the position of the newline character ("\n") after the YouTube link
        youtube_link_end = meal_text.search("\n", youtube_link_start, tk.END)

        # Check if the newline character is found
        if youtube_link_end:
            # Extract the YouTube link from the text and remove leading/trailing spaces
            link = meal_text.get(youtube_link_start, youtube_link_end).strip()

            # Open the extracted YouTube link in a web browser
            open_link(link)


def open_link(link):
    # Function to open the provided link in a web browser
    webbrowser.open(link)

# Function to search for a meal based on user input
def search_meal():
    # Retrieve the user's input from the search bar
    query = search_var.get()

    # Check if the user entered a query
    if query:
        # Construct the URL for the API request using the users query
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"

        # Make an http request to the API
        response = requests.get(url)

        # check the JSON response
        data = response.json()

        # Check if the API returned any meals
        if data["meals"]:
            # Display details for the first meal in the response
            meal = data["meals"][0]
            display_meal_details(meal)
        else:
            # If no meals were found display a message
            clear_labels("No meal found.")
    else:
        # If the user did not enter a search term display a message
        clear_labels("Please enter a search term.")

# Function to display a random meal
def randomize_meal():
    # Define the URL for fetching a random meal from The Meal DB API
    url = "https://www.themealdb.com/api/json/v1/1/random.php"

    # Send a request to the API and check the JSON response
    response = requests.get(url)
    data = response.json()

    # Check if the "meals" key exists in the response data
    if data["meals"]:
        # Extract the first meal from the list (since it's a random meal)
        meal = data["meals"][0]

        # Display detailed information about the random meal
        display_meal_details(meal)
    else:
        # If no random meal is found, display a message
        clear_labels("No random meal found.")


# Function to clear the displayed labels and show a custom message
def clear_labels(message):
    # Enable the Text widget for editing
    meal_text.config(state=tk.NORMAL)

    # Delete existing content in the Text widget
    meal_text.delete("1.0", tk.END)

    # Insert the provided message at the end of the Text widget
    meal_text.insert(tk.END, message)

    # Disable the Text widget for editing
    meal_text.config(state=tk.DISABLED)


# Creating the main Tkinter window
root = tk.Tk()
root.geometry("1500x1000+200+0")
root.maxsize(1500, 1000)
root.minsize(1500, 1000)
root.title("Meal Maker")
root.config(padx=60, pady=10, bg="#FFE4C4")

# Load the background image
bg_image = ImageTk.PhotoImage(Image.open("bg1.png"))
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Creating and displaying the title label
title_label = tk.Label(root, text="", bg="#FFE4C4", fg="#8B4513", font=('Arial black', 35, 'bold'))
title_label.pack(pady=(0, 1))

# Creating and displaying the placeholder image label
placeholder_image = Image.new("RGB", (200, 200), color="#FFE4C4")
placeholder_image = ImageTk.PhotoImage(placeholder_image)

dish_image_label = tk.Label(root, image=placeholder_image)
dish_image_label.pack(pady=(160,30), expand=False)  # Add top padding here

# Creating and displaying the search entry with placeholder text
search_var = tk.StringVar()
search_entry = tk.Entry(root, textvariable=search_var, font=("Arial", 15), bg="#FFE4C4", fg="#8B4513")
search_entry.insert(0, "Search bar")
search_entry.bind("<FocusIn>", lambda event: search_entry.delete(0, "end"))
search_entry.pack(pady=5, fill="both", expand=False)

# Creating and displaying the button frame
button_frame = tk.Frame(root, bg="#FFE4C4")
button_frame.pack(pady=5, fill="both", expand=False)

# Creating and displaying the search button
search_button = tk.Button(button_frame, text="Search", command=search_meal, font=("Montserrat", 15, 'bold'), bg="#8B4513", fg="#FFE4C4", width=15)
search_button.pack(pady=5, fill="both")

# Creating and displaying the randomize button
randomize_button = tk.Button(button_frame, text="Randomize", command=randomize_meal, font=("Montserrat", 15, 'bold'), bg="#8B4513", fg="#FFE4C4", width=15)
randomize_button.pack(pady=5, fill="both")

# Creating and displaying the body frame
body_frame = tk.Frame(root, bg="#FFE4C4")
body_frame.pack(fill="both", expand=True)

# Creating and displaying the meal text area
meal_text = tk.Text(body_frame, bg="#FFE4C4", fg="#8B4513", font=("Arial", 15, 'bold'), wrap="word", state=tk.DISABLED)
meal_text.pack(pady=(2, 0), side="left", fill="both", expand=True)

# Configuring tags for text alignment and link handling
meal_text.tag_configure("center", justify="center")
meal_text.tag_configure("youtube_link", foreground="blue", underline=True, justify="center")
meal_text.tag_bind("youtube_link", "<ButtonRelease-1>", on_click)

# Running the Tkinter main loop
root.resizable(True, True)
root.mainloop()
