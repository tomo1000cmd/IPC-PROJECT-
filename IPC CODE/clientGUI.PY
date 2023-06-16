import socket
import tkinter as tk
import webbrowser
import time
import matplotlib.pyplot as plt
# Server configuration
HOST = 'localhost'
PORT = 8888

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))
timestamps = []
speeds = []
# Function to update the GUI label and display colored square boxes
def update_label():
    start_time = time.time()
    # Receive data from the server
    received_data = client_socket.recv(1024).decode()
    end_time = time.time()
      # Calculate communication speed
    speed = end_time - start_time
        # Store timestamp and speed values
    timestamps.append(end_time)
    speeds.append(speed)

   # Split the received data into individual values
    available_spaces = [int(space) if space else 0 for space in received_data.split(',')]
    # Update the label with received data
    label.config(text=f'Available parking spaces:\n\nPARKING FACILITY: {available_spaces[0]}/50\n\nEV GRID: {available_spaces[1]}/20\n\nOPEN STREET: {available_spaces[2]}/20')
    
    # Clear the canvas
    canvas.delete("all")
    
    # Display square boxes for each section
    sections = len(available_spaces)
    max_spaces = [50, 20, 20]
    box_size = 20
    x_start = 20
    y_start = 50
    
    for section in range(sections):
        total_spaces = max_spaces[section]
        for i in range(total_spaces):
            x = x_start + (i % 10) * box_size
            y = y_start + (section * 120) + (i // 10) * box_size
            if i < available_spaces[section]:
                # Display green boxes for available spaces
                canvas.create_rectangle(x, y, x + box_size, y + box_size, fill="green", tags=("box",))
            else:
                # Display red boxes for occupied spaces
                canvas.create_rectangle(x, y, x + box_size, y + box_size, fill="red", tags=("box",))
    
    # Bind click event to the green boxes
    canvas.tag_bind("box", "<Button-1>", box_clicked)
    
    # Schedule the next update after 1 second (1000 milliseconds)
    root.after(1000, update_label)
   
# Plot the communication speed graph
    plt.plot(timestamps, speeds)
    plt.xlabel('Timestamp')
    plt.ylabel('Communication Speed (seconds)')
    plt.title('Communication Speed between Client and Server')
    plt.show()
# Function to handle the box click event
def box_clicked(event):
    # Get the clicked box item
    item = canvas.find_closest(event.x, event.y)
    
    # Check if the clicked item is in the list of canvas items
    if item and len(item) > 0:
        # Get the index of the clicked box
        index = int(item[0]) - 1
        
        # Determine the section based on the index
        section = ""
        if index < 50:
            section = "PARKING FACILITY: Available parking spaces"
        elif index < 70:
            section = "EV GRID: Electric grid parking"
        else:
            section = "OPEN STREET: Open street parking"
        
        # Open the web page link associated with the clicked box
        if section == "PARKING FACILITY: Available parking spaces":
            web_page_link = "https://www.google.com/maps/dir/51.9875892,5.9812832/NewMotion+Charging+Station,+Ruitenberglaan+29,+6826+CC+Arnhem/@51.9910664,5.9543369,2415m/data=!3m2!1e3!4b1!4m10!4m9!1m1!4e1!1m5!1m1!1s0x47c7a465eb955517:0xf865b4990b983dc3!2m2!1d5.9481747!2d51.9897422!3e0!5m1!1e1?entry=ttu"
        elif section == "EV GRID: Electric grid parking":
            web_page_link = "https://www.google.com/maps/place/Streetplug+Charging+Station/@51.9680899,5.944256,15z/data=!4m6!3m5!1s0x47c7a410969a14f1:0xa8a296bedf69c0e7!8m2!3d51.9680899!4d5.944256!16s%2Fg%2F11h3g71sn0?entry=ttu"
        else:
            section == "OPEN STREET: Open street parking"
            web_page_link = "https://www.google.com/maps/place/Reinaldstraat+22,+6824+GN+Arnhem/@51.9887978,5.9418843,3a,75y,227.34h,90t/data=!3m6!1e1!3m4!1shhmdCrLHXLTwPCjpYvue6Q!2e0!7i16384!8i8192!4m7!3m6!1s0x47c7a467defe8c2d:0x83010f1f97f086df!8m2!3d51.9887282!4d5.9418926!10e5!16s%2Fg%2F11c1_7z8p0!5m1!1e1?entry=ttu"
        
        webbrowser.open(web_page_link)

# Create the GUI window
root = tk.Tk()
root.title('IPC Application')

# Create a label to display the received data
label = tk.Label(root, text='Waiting for data...', font=('Arial', 14))
label.pack(padx=20, pady=10)

# Create a canvas to display the square boxes
canvas = tk.Canvas(root, width=250, height=400)
canvas.pack(padx=20, pady=10)

# Start updating the label and display
update_label()

# Start the GUI event loop
root.mainloop()

# Close the connection
client_socket.close()
