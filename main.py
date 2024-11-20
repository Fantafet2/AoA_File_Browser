'''
   to be done: 
    - add error handling for invalid file paths
    - sort files by different attributes(date modified, size)
    - get the drive based on the operating system
    - find a faster method to get all the files from the drive
           - add a loading screen to buffer the waiting time

    test directory ="C:/Users/franc/Documents/UTECH/2024 SEM 1/PHYSICS SEM 1 2024/physics/physics/labs"
'''

from PIL import Image
import os
import customtkinter
import time
import platform
import win32api
import re
import time
import mimetypes
import uuid
from fuzzywuzzy import fuzz
from tqdm import tqdm
import threading
import gpt_text_summary
import gpt_image_summary
import asyncio


def type_to_summarize(path,file_type, filename):
    text_types = {
        "text/plain", "text/html", "text/css", "text/csv", "text/xml",
        "application/json", "application/javascript", "application/rtf",
        "text/markdown"
    }

    image_types = {
        "image/jpeg", "image/png", "image/gif", "image/bmp",
        "image/tiff", "image/webp", "image/svg+xml", "image/x-icon"
    }


    # Determine the type
    if file_type in text_types:
        summary = gpt_text_summary.ai_text_response_type(path,filename)
    elif file_type in image_types:
        summary = gpt_image_summary.get_visual_features(path,filename)
    else:
        summary = "unknown"

    return summary


def get_mime_type(path,file_name):
  file_path = os.path.join(path,file_name)
  
  #mime = magic.from_file(file_path, mime=True)
  mime_type, _ = mimetypes.guess_type(file_path)

  return mime_type


def get_size_of_file(path,file_name):

    file_path = os.path.join(path,file_name)

    if os.path.exists(file_path):
        stat = os.stat(file_path)
        return stat.st_size
    
    else:
        print(f"File '{file_path}' not found.")
        return None

def get_last_modified_of_file(path,file_name):

    file_path = os.path.join(path,file_name)
    # Get last modification
    mod_time = os.path.getmtime(file_path)

    # Convert time to readable format
    mod_time_readable = time.ctime(mod_time)

    return mod_time_readable


def button_click(path,file_name):
    file_path = os.path.join(path,file_name)
    
    print("this is working... ", file_path)
    
    if os.path.exists(file_path):
        open_test_file(file_path)

def check_dir_or_file(layout_frame,path,num_buttons,file_name):
    print("this is the file name ",file_name)
    print(" ")
    print("this is the path ",path)
    print(" ")

    file_path = os.path.join(path,file_name)

    print("this is the file path", file_path)


    if os.path.isdir(file_path):

        print("This is a directory")

        dir_list = os.listdir(file_path)
        num_buttons = len(dir_list)

        show_files(file_path,num_buttons,dir_list)

    elif os.path.isfile(file_path):

        print("This is a file")
        button_click(path,file_path)
    else:
        print("File or directory not found")
        return False 


def clear_layout_frame():
    for widget in layout_frame.winfo_children():
            widget.destroy()
            
def create_layout_frame():

    global layout_frame

    layout_frame = customtkinter.CTkScrollableFrame(master=root)
    layout_frame.pack(fill="both", expand=True)

def show_files(path,num_buttons,dir_list):
    print("===================================")
    layout_frame.pack(side="top", anchor="center",padx=0,pady=0)

    layout_frame.grid_columnconfigure(0, weight=1, minsize=100, pad=10)
    layout_frame.grid_columnconfigure(1, weight=1, minsize=100, pad=10)
    layout_frame.grid_columnconfigure(2, weight=1, minsize=100, pad=10)
    layout_frame.grid_columnconfigure(3, weight=1, minsize=100, pad=10)
    layout_frame.grid_columnconfigure(4, weight=1, minsize=100, pad=10)

    lable_filename = customtkinter.CTkLabel(master = layout_frame, text = "File Name")
    lable_filename.grid(row=0, column=0, sticky="ew", pady=9)

    lable_fileSize = customtkinter.CTkLabel(master = layout_frame, text = "File Size")
    lable_fileSize.grid(row=0, column=1, sticky="ew", pady=9)

    lable_lastModified = customtkinter.CTkLabel(master = layout_frame, text = "Last Modifed")
    lable_lastModified.grid(row=0, column=2, sticky="ew", pady=9)

    lable_fileType = customtkinter.CTkLabel(master = layout_frame, text = "File Type")
    lable_fileType.grid(row=0, column=3, sticky="ew", pady=9)

    label_summary = customtkinter.CTkLabel(master = layout_frame, text = "File Summary")
    label_summary.grid(row=0, column=4, sticky="ew", pady=9)


    for i in range(num_buttons):
        button = customtkinter.CTkButton(master=layout_frame,width=40, text= os.path.basename(dir_list[i]), command=lambda i=i, dir_list=dir_list: check_dir_or_file(layout_frame,path,num_buttons, dir_list[i]))
        button.grid(row=i+1, column=0, sticky="ew")
        button.grid(row=i+1, column=0, sticky="ew", pady=9)

        file_size_label = customtkinter.CTkLabel(master=layout_frame, text=get_size_of_file(path,dir_list[i]))
        file_size_label.grid(row=i+1, column=1, sticky="ew")
        file_size_label.grid(row=i+1, column=1, sticky="ew", pady=9)

        
        file_path = os.path.join(path,dir_list[i])
        if os.path.exists(file_path):            
            if os.path.isfile(file_path):
                try:
                    file_last_modified_label = customtkinter.CTkLabel(master=layout_frame,text = get_last_modified_of_file(path,dir_list[i]))
                    file_last_modified_label.grid(row=i+1, column=2, sticky="ew")
                    file_last_modified_label.grid(row=i+1, column=2, sticky="ew", pady=9)

                    file_type = get_mime_type(path,dir_list[i])
                    file_type_label = customtkinter.CTkLabel(master=layout_frame, text=file_type)
                    file_type_label.grid(row=i+1, column=3, sticky="ew")
                    file_type_label.grid(row=i+1, column=3, sticky="ew", pady=9)

                    file_summary_label = customtkinter.CTkLabel(master=layout_frame, text= type_to_summarize(path,file_type,dir_list[i]))
                    file_summary_label.grid(row=i+1, column=4, sticky="ew")
                    file_summary_label.grid(row=i+1, column=4, sticky="ew", pady=9)
    
                   
                        
                except FileNotFoundError:
                    print(f"File '{file_path}' not found.")
                except PermissionError:
                    print(f"Permission denied to access '{file_path}'.") 

                except OSError as e:
                    print(f"An error occurred while opening the file: {e}")
                        

def open_all_files():

    path = "C:/Users/franc/Documents/UTECH/2024 SEM 1/PHYSICS SEM 1 2024/physics/physics/labs"
    #the name of what is being opened
    dir_list = os.listdir(path)

    num_of_files = len(dir_list)
    print(num_of_files)

    clear_layout_frame()
    clear_layout_frame()
    show_files(path,num_of_files,dir_list)

def open_test_file(file_path):

    # check if file exists then opens it in default application
    if os.startfile(file_path):
        return
    
    
def get_drive_path(drive_letter):
    if len(drive_letter) != 2 or drive_letter[1] != ':':
        return None

    return drive_letter + "//"

def get_windows_drive(): 
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('//00')
    
    return [drive[:-2] for drive in drives if drive]

#checks the type of operating system
def get_os_name():
    # Get operating system name 
    os_name = platform.system()

    if os_name== "Windows":
    # Windows-specific code
        drive = get_windows_drive()
    elif os_name == "Linux":
        # Linux-specific code
        print("Running on Linux")
    elif os_name == "Darwin":
        # macOS-specific code
        print("Running on macOS")
    else:
        print("Unknown operating system")

    return drive

contains = []
id_ = uuid.uuid4()

def check_layout_frame_exist(drive,num_of_files,dir_list):

    clear_layout_frame()

    print("this is drive: ",drive)
    print("this is num of: ",num_of_files)
    print("this is dir list: ",dir_list)
    
    show_files(drive,num_of_files,dir_list)

def search_for_file_in_drive(file_type,drive,substring):
    
    dir_list = []

    for name in store_all_files:
        file_name = os.path.basename(name)
        if name.endswith(tuple(ft for ft in file_type)) or file_type == "":
            if substring.lower() in file_name.lower():
                print("this is the path: ",name)

                dir_list.append(name)
    num_of_files = len(dir_list)

    for name in store_all_files:
        file_name = os.path.basename(name)
        if name.endswith(tuple(ft for ft in file_type)) or file_type == "":
            if substring.lower() in file_name.lower():
                print("this is the path: ",name)

                dir_list.append(name)
    num_of_files = len(dir_list)

    check_layout_frame_exist(drive,num_of_files,dir_list)

    check_layout_frame_exist(drive,num_of_files,dir_list)

    print("fininshed searchingn")
    


                    

def open_file():

    #creates the path to the drive
    drives = get_os_name()
    print("this is the drive path: ", drives[0])

    for drive in drives:

        drive_path = get_drive_path(drive)
        print(f"Main directories on {drive} : {drive_path}")


        if os.path.exists(drive_path):

            '''open_test_file(drive_path)'''
            #the name of what is being opened
            dir_list = os.listdir(drive_path)
            
            py_dir_list = []
            for dir_name in dir_list:
                new_dir_name = re.sub(r"\\", "//", dir_name)
                py_dir_list.append(new_dir_name)            
            
            num_of_files = len(dir_list)
            
            clear_layout_frame()
            clear_layout_frame()
            show_files(drive_path,num_of_files,dir_list)
    

 
def search_files(search_text):

    drives = get_os_name()

    for drive in drives:

        drive_path = get_drive_path(drive)

    for root, dir, files in os.walk(drive_path):
        for file in files:
            file_path = os.path.join(root, file)
            if search_text.lower() in file.lower():
                print(f"File found: {file_path}")
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if search_text.lower() in line.lower():
                            print(file_path)
                            break

#Creates the opening page of the application
def create_frane():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    #creates the application window
    global root 
    root = customtkinter.CTk()
    root.geometry("1250x700")

    global frame
    frame= customtkinter.CTkScrollableFrame(master = root)
    frame.pack(pady = 20, padx = 60, fill = "both", expand = True)

    #setting the values for the columns on the main frame
    frame.grid_columnconfigure(0, weight=1, minsize=100, pad=30)
    frame.grid_columnconfigure(1, weight=1, minsize=100, pad=10)
    frame.grid_columnconfigure(2, weight=1, minsize=100, pad=10)


    #Entry feilds to search for a file 
    #this specifies the file type but is not neccesarry
    search_file_type = customtkinter.CTkEntry(master = frame, width=50, placeholder_text="Search files")
    search_file_type.grid(row=1, column=1, sticky="ew", pady=30)

    #Entry feild for the file name
    fuzzy_search_keyword = customtkinter.CTkEntry(master = frame, width= 50, placeholder_text="Enter fuzzy search")
    fuzzy_search_keyword.grid(row=1, column=0, sticky="ew", pady=9)


    '''get_drive_to_search = get_os_name()
    drive_to_search = get_drive_to_search[0]+'/'''
    drive_to_search = "C:/Users/franc/Documents/UTECH/2024 SEM 1/PHYSICS SEM 1 2024/physics/physics/labs"
    button = customtkinter.CTkButton(master = frame, text = "Search", command=lambda: search_for_file_in_drive(search_file_type.get(),drive_to_search,fuzzy_search_keyword.get()))
    button.grid(row=1, column=2, sticky="ew", pady=9)

    label = customtkinter.CTkLabel(master = frame, text = "file explorer")
    label.grid(row=0, column=1, sticky="ew", pady=9)


    button = customtkinter.CTkButton(master =frame, text = "Open Drive", command=open_file)
    button.grid(row=2, column=0, sticky="ew", pady=9)

    create_layout_frame()

    root.mainloop()


def get_all_files_from_file():

    get_drive_to_search = get_os_name()
    drive = get_drive_to_search[0]+'/'
    
    global store_all_files
    store_all_files = []

    file_type = ""
   

    for root, dirs, files in tqdm(os.walk(drive), desc="Searching for files..."):
        for file in files:
                file_path = os.path.join(root, file)
                store_all_files.append(file_path)
                        

    print("all files have been stored")
    print("total number of files: ", len(store_all_files))


def main():

    thread1 = threading.Thread(target=get_all_files_from_file)
    thread2 = threading.Thread(target=create_frane)
    
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()
   
if __name__ == "__main__":
    main()
