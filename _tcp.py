from _mta import Mta6_Data
from _mta import prepare_sending_data
import tkinter as tk
import socket
import threading

def connect_and_send(ip_address, port, id, lat, lon, speed, run):
    try:
        # Connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        output_field.insert(tk.END, "Connect Status: OK\n") 

        #prepare data
        binary_data = prepare_sending_data(lat, lon, speed, run)
        send_data = "id=" + id + "&bin="
        final_data = send_data.encode() + binary_data

        # Sending Header
        post_data = "POST gp.dll?data HTTP/1.1\r\nContent-Length:{}\r\n\r\n".format(len(final_data))
        output_field.insert(tk.END, post_data)
        client_socket.sendall(post_data.encode())
        #Get 1st response
        response = client_socket.recv(1024).decode()
        output_field.insert(tk.END, "Response: " + response + "\n")
        #output
        for byte in final_data:
            output_field.insert(tk.END, hex(byte)+" ")
        output_field.insert(tk.END, "\nSending Data...\n")    
        client_socket.sendall(final_data)
        output_field.insert(tk.END, "DONE!\n")
        #Get 2nd response
        response = client_socket.recv(1024).decode()
        output_field.insert(tk.END, "Response: " + response)
        # Close Connect
        client_socket.close()
        output_field.insert(tk.END, "\nConnection is closed \n")
    except socket.timeout:
        output_field.insert(tk.END, "Socket timeout occurred\n")
    except Exception as e:
        output_field.insert(tk.END, "ERROR: " + str(e) + "\n")  
 

def on_submit():
    output_field.delete(1.0, tk.END)
    ip_address = ip_input_field.get()
    if not ip_address:
        output_field.insert(tk.END, "IP IS EMPTY!")
        return

    port = port_input_field.get()
    if not port:
        output_field.insert(tk.END, "PORT IS EMPTY!")
        return
    else:
        port = int(port)
    
    id = id_input_field.get()
    if not id:
        output_field.insert(tk.END, "DEVICE ID IS EMPTY!")
        return
    
    lat = lat_input_field.get()
    try: 
        lat = float(lat)
    except:
        lat = 0.0
        lat_input_field.insert(tk.END, "0.0")
    
    lon = lon_input_field.get()
    try: 
        lon = float(lon)
    except:
        lon = 0.0
        lon_input_field.insert(tk.END, "0.0")
    
    speed = speed_input_field.get()
    if not speed:
        speed = 0
        speed_input_field.insert(tk.END, "0")
    else:
        speed = int(speed)

    run = run_input_field.get()
    if not run:
        run = 0
        run_input_field.insert(tk.END, "0")
    else:
        run = int(run)

    output_field.delete(1.0, tk.END)  # Clear Output
    # New thread for I/O
    thread = threading.Thread(target=connect_and_send, args=(ip_address, port, id, lat, lon, speed, run))
    thread.start()

def connect():
    output_field.delete(1.0, tk.END)
    
    ip_address = ip_input_field.get()
    if not ip_address:
        output_field.insert(tk.END, "IP IS EMPTY!")
        return
    
    port = port_input_field.get()
    if not port:
        output_field.insert(tk.END, "PORT IS EMPTY!")
        return
    else:
        port = int(port)
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        output_field.insert(tk.END, "Connecting...")
        client_socket.connect((ip_address, port))
        output_field.insert(tk.END, "Connect Status: OK\n")
        client_socket.close()
        output_field.insert(tk.END, "Connection is closed \n")
    except socket.timeout:
        output_field.insert(tk.END, "Socket timeout occurred\n")
    except Exception as e:
        output_field.insert(tk.END, "ERROR: " + str(e) + "\n")  

def paste(event):
    widget = root.focus_get()
    if isinstance(widget, tk.Text):
        text = root.clipboard_get()
        widget.insert(tk.INSERT, text)
    

root = tk.Tk()
root.title("MTA6_TCP")

#Fix window size
root.geometry("1050x600")
root.resizable(width=False, height=False)

#IP
ip_input_field = tk.Entry(root, highlightthickness=1, highlightbackground="black")
ip_input_field.grid(row=0, column=1, padx=20, pady=5, sticky=tk.W) 
ip_input_field.config(width=40) 
#Latitude
lat_input_field = tk.Entry(root, highlightthickness=1, highlightbackground="black")
lat_input_field.grid(row=0, column=4, padx=10, pady=5, sticky=tk.E)

#Port
port_input_field = tk.Entry(root, highlightthickness=1, highlightbackground="black")
port_input_field.grid(row=1, column=1, padx=20, pady=5, sticky=tk.W) 
port_input_field.config(width=8)

#Longitude
lon_input_field = tk.Entry(root, highlightthickness=1, highlightbackground="black")
lon_input_field.grid(row=1, column=4, padx=10, pady=5, sticky=tk.E)
lon_input_field.config(width=20)

#Device ID
id_input_field = tk.Entry(root, highlightthickness=1, highlightbackground="black")
id_input_field.grid(row=2, column=1, padx=20, pady=5, sticky=tk.W)  
id_input_field.config(width=50)

#Car speed
speed_input_field = tk.Entry(root, highlightthickness=1, highlightbackground="black")
speed_input_field.grid(row=2, column=4, padx=10, pady=5, sticky=tk.E)

#Car RUN
run_input_field = tk.Entry(root, highlightthickness=1, highlightbackground="black")
run_input_field.grid(row=3, column=4, padx=10, pady=5, sticky=tk.E)
#run_input_field.config(width=20)

#Main Output
output_field = tk.Text(root, highlightthickness=2, highlightbackground="gray")
output_field.grid(row=4, column=1, columnspan=4, padx=10, pady=3, sticky=tk.NS) 
output_field.config(width=120, height=25) 

#Ctrl+V enable
root.bind("<Control-v>", paste)

#Labels
ip_label = tk.Label(root, text="IP")
ip_label.grid(row=0, column=0, sticky=tk.W) 
lat_label = tk.Label(root, text="Latitude")
lat_label.grid(row=0, column=4, sticky=tk.W, padx=(113, 2))
port_label = tk.Label(root, text="Port")
port_label.grid(row=1, column=0, sticky=tk.W)  
lon_label = tk.Label(root, text="Longitude")
lon_label.grid(row=1, column=4, sticky=tk.W, padx=(102, 2)) 
id_label = tk.Label(root, text="ID")
id_label.grid(row=2, column=0, sticky=tk.W)
speed_label = tk.Label(root, text="Speed")
speed_label.grid(row=2, column=4, sticky=tk.W, padx=(123, 2)) 
run_label = tk.Label(root, text="RUN")
run_label.grid(row=3, column=4, sticky=tk.W, padx=(133, 2)) 

# Button Submit
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.grid(row=5, column=4, ipadx=20, padx=50, pady=10, rowspan=2, sticky=tk.W)

#Button Check Connect
check_connect_button = tk.Button(root, text="Check Connect", command=connect)
check_connect_button.grid(row=5, column=4, ipadx=25, padx=7, pady=10, rowspan=2, sticky=tk.E)

label_output_text = tk.Label(root, text="Output")
label_output_text.grid(row=4, column=0, sticky=tk.NW)
root.mainloop()

