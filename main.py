import customtkinter as ctk
import sys
import os
import shutil
from distutils.dir_util import copy_tree
from datetime import date
from zipfile import ZipFile
import time
import logging
import subprocess


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Ui(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.d_home_dir = os.getcwd()
        self.d_log = os.path.join(self.d_home_dir, "log.txt")
        self.d_config_file = "C:\\Users\\PC\\AppData\\Roaming\\bakkesmod\\bakkesmod\\cfg\\plugins.cfg"
        self.d_config_backup = os.path.join(self.d_home_dir,"cfg_Backup\\config backup")
        self.d_data_dir = "C:\\Users\\PC\\AppData\\Roaming\\bakkesmod\\bakkesmod\\data"
        self.d_uninstalled = os.path.join(self.d_home_dir,"uninstalled plugins")
        self.d_plugins_dir = "C:\\Users\\PC\\AppData\Roaming\\bakkesmod\\bakkesmod\plugins"
        self.d_settings_dir = "C:\\Users\\PC\\AppData\\Roaming\\bakkesmod\\bakkesmod\\plugins\\settings"

        self.home_dir = os.getcwd()
        self.log = os.path.join(self.home_dir, "log.txt")
        self.config_file = "C:\\Users\\PC\\AppData\\Roaming\\bakkesmod\\bakkesmod\\cfg\\plugins.cfg"
        self.config_backup = os.path.join(self.home_dir,"cfg backup")
        self.data_dir = "C:\\Users\\PC\\AppData\\Roaming\\bakkesmod\\bakkesmod\\data"
        self.uninstalled = os.path.join(self.home_dir,"uninstalled plugins")
        self.plugins_dir = "C:\\Users\\PC\\AppData\Roaming\\bakkesmod\\bakkesmod\plugins"
        self.settings_dir = "C:\\Users\\PC\\AppData\\Roaming\\bakkesmod\\bakkesmod\\plugins\\settings"

        self.t_plugins = os.path.join(self.home_dir, "Test\plugins")
        self.t_settings = os.path.join(self.home_dir, "Test\plugins\settings")
        self.t_data = os.path.join(self.home_dir, "Test\data")
        self.t_config = os.path.join(self.home_dir, "Test\cfg\plugins.cfg")
        self.installed = []
        self.backup = False
        self.reset_textbox = False
        self.test = False
        self.unzip = False
        self.open = False

        #window
        self.geometry("800x500")
        self.title("Bakkes Mod Plugin installer")
    

        #configuring grids
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight=1)


        #self.mainframe.grid_rowconfigure(0, weight=1)
        #self.mainframe.grid_rowconfigure(1, weight=1)
        #self.mainframe.grid_rowconfigure(2, weight=1)

        # Placing frames and buttons

        self.grid_columnconfigure(0, weight=1, )
        self.grid_columnconfigure(1, weight=1, )
        self.grid_columnconfigure(2, weight=1, )
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        # self.grid_rowconfigure(2, weight=10)

        self.frame_top = ctk.CTkFrame(master=self, corner_radius=25)
        self.frame_top.grid(row=0,column=1, sticky="nsew", padx=10, pady=10, columnspan=2)

        self.frame_top.grid_columnconfigure(0,weight=1)
        self.frame_top.grid_rowconfigure(0,weight=1)

        self.textbox = ctk.CTkTextbox(master=self.frame_top, text_color="green", width=500, corner_radius=25)
        self.textbox.grid(row=0, column=0)


        


        self.frame_left = ctk.CTkFrame(self, width=140, corner_radius=25)
        self.frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10,rowspan = 3)

        self.frame_left.grid_rowconfigure(0,weight=1)
        self.frame_left.grid_rowconfigure(1,weight=1)
        self.frame_left.grid_rowconfigure(2,weight=1)
        self.frame_left.grid_rowconfigure(3,weight=1)
        self.frame_left.grid_rowconfigure(4,weight=1)
        self.frame_left.grid_columnconfigure(0, weight= 1)

        #code for adjusting tthe Apearance of UI
        self.apearnce_label = ctk.CTkLabel(master=self.frame_left, text="Apearance Mode:", font=ctk.CTkFont(size=15, weight="bold"))
        self.apearnce_label.grid(row=0, padx=20, pady=(20, 10), sticky="s")

        self.apearance_mode_menue = ctk.CTkOptionMenu(master=self.frame_left, values=["System", "Light", "Dark" ], command=self.change_appearance_mode)
        self.apearance_mode_menue.grid(row=1, column=0, pady=20)

        self.extra_label = ctk.CTkLabel(master=self.frame_left, text="Extra:", font=ctk.CTkFont(size=15, weight="bold"))
        self.extra_label.grid(row=2, padx=20, sticky="s")

        self.defaults = ctk.CTkButton(master=self.frame_left, text = "load default Paths", font=ctk.CTkFont(size=12, weight="bold"), height=50, width=85, command=self.set_default_paths)
        self.defaults.grid(row=3, column = 0, pady=10)

        self.exit_button = ctk.CTkButton(master=self.frame_left, text = "EXIT", font=ctk.CTkFont(size=15, weight="bold"), command=self.exit_onclick, height=50, width=85)
        self.exit_button.grid(row=4, column = 0, pady=10)

        self.frame_midle = ctk.CTkFrame(master=self, corner_radius=25)
        self.frame_midle.grid(row=1,column=1,rowspan = 2, sticky="nesw", padx=10, pady=10)

        self.frame_midle.grid_rowconfigure(0, weight=1)
        self.frame_midle.grid_rowconfigure(1, weight=1)
        self.frame_midle.grid_rowconfigure(2, weight=1)
        self.frame_midle.grid_rowconfigure(3, weight=1)
        self.frame_midle.grid_rowconfigure(4, weight=1)
        self.frame_midle.grid_rowconfigure(5, weight=1)
        self.frame_midle.grid_columnconfigure(0, weight=1)

        #assigning folders
        self.folders_label = ctk.CTkLabel(master=self.frame_midle, text="Paths:", font=ctk.CTkFont(size=15, weight="bold"))
        self.folders_label.grid(row=0,)

        self.plugins_entry= ctk.CTkEntry(master=self.frame_midle,width=280, placeholder_text="instalplugins Folder")
        self.plugins_entry.grid(row=1, column=0)

        self.settings_entry= ctk.CTkEntry(master=self.frame_midle, placeholder_text="settings Folder",width=280)
        self.settings_entry.grid(row=2, column=0)

        self.data_entry= ctk.CTkEntry(master=self.frame_midle, placeholder_text="Data Folder",width=280)
        self.data_entry.grid(row=3, column=0)

        self.cfg_entry= ctk.CTkEntry(master=self.frame_midle, placeholder_text="Config File",width=280)
        self.cfg_entry.grid(row=4, column=0)

        self.uninstalled_plugins_entry= ctk.CTkEntry(master=self.frame_midle, placeholder_text="Uninstaled plugins",width=280)
        self.uninstalled_plugins_entry.grid(row=5, column=0)

        


        #script settings
        self.frame_right = ctk.CTkFrame(master=self, corner_radius=25)
        self.frame_right.grid(row=1,column=2, rowspan=2, sticky="nesw", padx=10, pady=10)

        self.frame_right.grid_rowconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(2, weight=1)
        self.frame_right.grid_rowconfigure(3, weight=1)
        self.frame_right.grid_rowconfigure(4, weight=1)
        self.frame_right.grid_rowconfigure(5, weight=1)
        self.frame_right.grid_rowconfigure(6, weight=1)
        self.frame_right.grid_columnconfigure(0,weight=1)

        
        self.options_label = ctk.CTkLabel(master=self.frame_right, text="Script Options:", font=ctk.CTkFont(size=15, weight="bold"))
        self.options_label.grid(row=0)

        self.swich1 = ctk.CTkSwitch(master=self.frame_right, text= "Backup config", command = lambda:self.backup_event(self.swich1))
        self.swich1.grid(row=1, column=0)

        self.swich2 = ctk.CTkSwitch(master=self.frame_right, text="Reset textbox", command = lambda:self.text_reset_event(self.swich2))
        self.swich2.grid(row=2, column=0)

        self.swich3 = ctk.CTkSwitch(master=self.frame_right, text="Test Mode", command = lambda:self.test_event(self.swich3))
        self.swich3.grid(row=3, column=0)

        self.chekbox1 = ctk.CTkCheckBox(master=self.frame_right, text="Open Bakkes mod after install", command = lambda:self.open_event(self.chekbox1))
        self.chekbox1.grid(row=4, column=0)

        self.chekbox2 = ctk.CTkCheckBox(master=self.frame_right, text="Unzip", command = lambda:self.unzip_event(self.chekbox2))
        self.chekbox2.grid(row=5, column=0)

        self.start_btn= ctk.CTkButton(master=self.frame_right, text = "Install", font=ctk.CTkFont(size=15, weight="bold"), command=lambda: self.get_entry_plugins(), height=50, width=100)
        self.start_btn.grid(row=6, column = 0, pady=10)

    #Functions
    def change_color(self, new_color):
        ctk.set_default_color_theme(new_color)  # Themes: "blue" (standard), "green", "dark-blue"
    
    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)  # Modes: "System" (standard), "Dark", "Light"

    def set_default_paths(self):
        self.plugins_entry.delete(0,ctk.END)
        self.plugins_entry.insert(0, self.d_plugins_dir)

        self.settings_entry.delete(0,ctk.END)
        self.settings_entry.insert(0, self.d_settings_dir)

        self.data_entry.delete(0,ctk.END)
        self.data_entry.insert(0, self.d_data_dir)

        self.cfg_entry.delete(0,ctk.END)
        self.cfg_entry.insert(0, self.d_config_file)

        self.uninstalled_plugins_entry.delete(0,ctk.END)
        self.uninstalled_plugins_entry.insert(0, self.uninstalled)
    
    def insert_text(self,text_entry,  text):
        #text_entry.delete(0,ctk.END)
        text_entry.insert(ctk.END, text)

    def install(self):
        if self.reset_textbox  is True:
            self.textbox.delete("1.0", ctk.END)

        if self.test  is True:
            self.insert_text(self.textbox, "Test mode enabled\n")
            self.insert_text(self.textbox, "Running in Test mode\n")
            self.plugins_dir = self.t_plugins
            self.settings_dir = self.t_settings
            self.data_dir = self.t_data
            self.config_file = self.t_config

        if self.backup is True:
            self.insert_text(self.textbox, "Backing up config.....\n")
            shutil.copy2(self.config_file, self.config_backup)
            self.insert_text(self.textbox, "Backed up in cgf backup \n")


        logging.basicConfig(filename=self.home_dir + "\\logs\\" + 'logs.log', level=logging.ERROR)

        try:
            plugins = os.listdir(self.uninstalled)
            if self.unzip is True:
                
                self.insert_text(self.textbox, "unziping file(s)\n")
                for plugin in plugins:
                    if plugin.endswith(".zip"):
                        with ZipFile(os.path.join(self.uninstalled, plugin), 'r') as zfile:
                            zfile.extractall(path=os.path.join(self.uninstalled, plugin.removesuffix(".zip")))
                plugins = os.listdir(self.uninstalled)

            self.insert_text(self.textbox, "Installing \n")

            
            for i in plugins:
                try:
                    if not i.endswith(".zip"):
                        installing = self.uninstalled + "\\" + i
                        #Chek for data folder and copy content
                        if "data" in os.listdir(installing):
                            for i in os.listdir(installing + "\\data"):
                                copy_tree(installing + "\\data\\" + i, self.data_dir)
                        #Copy plugin
                        for dll in os.listdir(installing + "\\plugins"):
                            if dll.endswith(".dll"):
                                shutil.copy2(installing + "\\plugins\\" + dll, self.plugins_dir)
                                self.installed.append(dll.removesuffix(".dll"))
                        #Chek for settings folder and copy contents 
                        if "settings" in os.listdir(installing + "\\plugins"):
                            for setting in os.listdir(installing + "\\plugins\\settings"):
                                if setting.endswith(".set"):
                                    shutil.copy2(installing + "\\plugins\\settings\\" + setting, self.settings_dir)

                except  PermissionError as e:
                    logging.exception(e)

            
            self.insert_text(self.textbox, "Installed " + str(len(self.installed)) + " plugins: ")
            for i in self.installed:
                self.insert_text(self.textbox, ", " + i )
            #updat config file
            with open(self.config_file, "a") as cfg:
                for name in self.installed:
                    cfg.write("\n" + "plugin load " + name)
            self.installed = []

        except FileNotFoundError as e:
            logging.exception(e)
        if self.open is True:
            self.insert_text(self.textbox, "\n\nOpening BakkesMod")
            subprocess.Popen('C:\\Program Files\\BakkesMod\\BakkesMod.exe')
    

    def exit_onclick(self):
        sys.exit(0)

    def backup_event(self, switch):
        #backup swich
        if switch == self.swich1 and self.backup is False:
            self.backup = True
        else: self.backup = False
        #log swich
    def text_reset_event(self, switch):
        if switch == self.swich2 and self.reset_textbox is False:
            self.reset_textbox = True
        else: self.reset_textbox = False
    def test_event(self, switch):
        if switch == self.swich3 and self.test is False:
            self.test = True
        else: self.test = False
    def open_event(self, switch):
        if switch == self.chekbox1 and self.open is False:
            self.open = True
        else: self.open = False
    def unzip_event(self, switch):
        if switch == self.chekbox2 and self.unzip is False:
            self.unzip = True
        else: self.unzip = False

    def get_entry_plugins(self):
        plugins = self.plugins_entry.get()
        settings = self.settings_entry.get()
        data = self.data_entry.get()
        config = self.cfg_entry.get()
        uni = self.uninstalled_plugins_entry.get()

        if plugins != "":
            self.plugins_dir = plugins

        
        if data != "":
            self.data_dir = data
        
        
        if settings != "":
            self.settings_dir = settings

        
        if config != "":
            self.config_file = config

        
        if uni != "":
            self.uninstalled = uni
        self.install()


if __name__== "__main__":
    ui = Ui()
    ui.mainloop()



#reset button: clears everything