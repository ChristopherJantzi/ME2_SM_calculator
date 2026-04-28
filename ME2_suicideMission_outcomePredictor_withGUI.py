import sys
import re
import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext
import tkinter.font as tkfont
import copy

'''----------------------------------------Constants, Flags, Options----------------------------------------
'''
stinger = True


'''----------------------------------------Functions and Classes----------------------------------------
'''
class Character:
	"""A ME2 Squadmate's Character Details"""
	def __init__(self, tier, loyal=False, ventPref=False, bioticPref=False, leaderPref=False, squad=False, recruited=True):
		self.loyal = tk.BooleanVar(value=loyal)
		self.ventPref = tk.BooleanVar(value=ventPref)
		self.bioticPref = tk.BooleanVar(value=bioticPref)
		self.leaderPref = tk.BooleanVar(value=leaderPref)
		self.squad = tk.BooleanVar(value=squad)
		self.tier = tk.BooleanVar(value=tier)
		self.recruited = tk.BooleanVar(value=recruited)

class Crew:
	"""The Status of the Crew"""
	def __init__(self, statusKnown=False, Dr=True, percent=100, missionsPrior=0):
		self.statusKnown = tk.BooleanVar(value=statusKnown)
		self.Dr = tk.BooleanVar(value=Dr)
		self.percent = tk.IntVar(value=percent)
		self.missionsPrior = tk.IntVar(value=missionsPrior)

def updateBoolVar(choice, var):
	yes = choice.get()
	var.set(yes == "Yes")

def updateSelections(choice1, choice2):
	if isinstance(choice1, str):
		selected1 = choice1
		selected2 = choice2.get()
	else:
		selected1 = choice1.get()
		selected2 = choice2.get()

	if (selected1 == selected2) and (selected1 != ""):
		choice2.set("")

def armorCheck(d):
	"""
	Purpose: Kill Jack if you fail the armor check

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs

	Return: N/A
	"""	
	if ("Jack" in d):
		del d["Jack"]

def shieldCheck(d):
	"""
	Purpose: Kill a crew member if you fail the shield check

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs

	Return: N/A
	"""	
	l = ["Kasumi", "Legion", "Tali", "Thane", "Garrus", "Zaeed", "Grunt", "Samara", "Morinth"]
	for i, v in enumerate(l):
		if (v in d) and (not d[v].squad.get()):
			del d[v]
			break

def weaponsCheck(d):
	"""
	Purpose: Kill a crew member if you fail the weapons check

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs

	Return: N/A
	"""	
	l = ["Thane", "Garrus", "Zaeed", "Grunt", "Jack", "Samara", "Morinth"]
	for i, v in enumerate(l):
		if (v in d) and (not d[v].squad.get()):
			del d[v]
			break

def toggleAvailable(s, name):
    d_all = s.allSquadmates
    d_surv = s.survivors
    checks = s.checkButtons
    c1 = s.squadCargo1_choice
    c2 = s.squadCargo2_choice
    s1 = s.squadCargo1_selector
    s2 = s.squadCargo2_selector

    if name == "Morinth":
        d_all["Morinth"].loyal.set(True)
        #d_surv["Morinth"] = d_all["Morinth"]

        d_all["Samara"].recruited.set(False)
        d_all["Samara"].loyal.set(False)
        checks["Samara"][1].config(state="disabled")

        if "Samara" in d_surv:
            del d_surv["Samara"]
            updateSelections("Samara", c1)
            updateSelections("Samara", c2)
    elif name == "Samara":
        #d_surv["Samara"] = d_all["Samara"]

        d_all["Morinth"].recruited.set(False)
        d_all["Morinth"].loyal.set(False)
        checks["Morinth"][1].config(state="disabled")
		
        if "Morinth" in d_surv:
            del d_surv["Morinth"]
            updateSelections("Morinth", c1)
            updateSelections("Morinth", c2)

    if d_all[name].recruited.get():
        checks[name][1].config(state="normal")
        d_surv[name] = d_all[name]
    else:
        d_all[name].loyal.set(False)
        checks[name][1].config(state="disabled")
        if name in d_surv:
            del d_surv[name]
            updateSelections(name, c1)
            updateSelections(name, c2)
    s.survivor_names = list(d_surv.keys())
    s.squadCargo1_selector["values"] = s.survivor_names
    s.squadCargo2_selector["values"] = s.survivor_names






class GUI():
    def __init__(self, root):
        self.root = root
        self.root.title("Jantzi's Super Wham-O-Dyne ME2 Suicide Mission Calculator!!!")
        self.root.geometry("1600x1000") # width x height

        self.allSquadmates = {"Grunt":Character(tier=3), "Zaeed":Character(tier=3), "Thane":Character(tier=1), "Legion":Character(ventPref=True, tier=1), "Garrus":Character(leaderPref=True, tier=3), "Jacob":Character(leaderPref=True, tier=1), "Miranda":Character(leaderPref=True, tier=1), "Jack":Character(bioticPref=True, tier=0), "Kasumi":Character(ventPref=True, tier=0), "Tali":Character(ventPref=True, tier=0), "Mordin":Character(tier=0), "Samara":Character(bioticPref=True, tier=1), "Morinth":Character(bioticPref=True, recruited=False, tier=1)}
        self.survivors = copy.copy(self.allSquadmates)
        del self.survivors["Morinth"]
        self.allSquadmates_names = list(self.allSquadmates.keys())
        self.survivor_names = list(self.survivors.keys())
        self.squadCargo_names = list(self.survivors.keys())

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f5", font=("Segoe UI", 11))
        style.configure("TCheckbutton", background="#f0f0f5", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)

        style.configure("raised.TFrame", background="#ffffff", borderwidth=20, relief="raised")
        style.configure("raised.TLabel", background="#ffffff", font=("Segoe UI", 11))
        style.configure("raised.TCheckbutton", background="#ffffff", font=("Segoe UI", 10))
        style.configure("raised.TButton", font=("Segoe UI", 11, "bold"), padding=6)





        ####################################### -------- Main Frame -------- #######################################
        mainFrame = ttk.Frame(root, padding=20)
        mainFrame.pack(fill="both", expand=True)      


        ####################################### -------- Options Frame -------- #######################################
        optionsFrame = ttk.Frame(mainFrame, padding=20)
        optionsFrame.pack(fill="both", expand=True)

        title = ttk.Label(optionsFrame, text="ME2 Suicide Mission Calculator", font=("Segoe UI", 24, "bold"))
        title.pack(pady=10)


        ### ----------------------------------------------- Character List and Checkboxes ----------------------------------------------- ###
        ### These take up the leftmost section of the GUI, towards the top
        rowStart = 0 	# Needs as many as crew exist
        colStart = 0 	# Needs 3

        charListFrame = ttk.Frame(optionsFrame, style="raised.TFrame")
        charListFrame.pack(pady=10, side='left')

        ttk.Label(charListFrame, text="Name", style="raised.TLabel").grid(row=rowStart, column=colStart, padx=5, pady=5, sticky="e")
        ttk.Label(charListFrame, text="Recruited", style="raised.TLabel").grid(row=rowStart, column=(colStart+1), padx=10, pady=5, sticky="w")
        ttk.Label(charListFrame, text="Loyal", style="raised.TLabel").grid(row=rowStart, column=(colStart+2), padx=10, pady=5, sticky="w")

        tempCounter = rowStart+1
        
        self.checkButtons = {}
        for i, name in enumerate(self.allSquadmates_names):

        	ttk.Label(charListFrame,
        		text=name,
        		style="raised.TLabel"
        	).grid(row=tempCounter, column=(colStart), padx=10, pady=5, sticky="e")

        	rec_button = ttk.Checkbutton(charListFrame,
        		variable=self.allSquadmates[name].recruited,
        		command=lambda name=name: toggleAvailable(self, name),
        		style="raised.TCheckbutton"
        	)

        	loy_button = ttk.Checkbutton(charListFrame,
        		variable=self.allSquadmates[name].loyal,
        		style="raised.TCheckbutton"
        	)
        	
        	if name == "Morinth":
        		loy_button.config(state="disabled")

        	self.checkButtons[name] = [rec_button, loy_button]
        	rec_button.grid(row=tempCounter, column=(colStart+1), padx=10, pady=5)
        	loy_button.grid(row=tempCounter, column=(colStart+2), padx=10, pady=5)

        	tempCounter += 1


        ### ----------------------------------------------- Prepwork and Cargo Bay Squad Select ----------------------------------------------- ###
        ### These take up the leftmost section of the GUI, towards the top
        rowStart = 0	# ???? These might be unnecessary for multiple frames
        colStart = 0 	# ????

        self.theCrew = Crew()
        self.upgradeArmor = tk.BooleanVar(value=False)
        self.upgradeShield = tk.BooleanVar(value=False)
        self.upgradeCannon = tk.BooleanVar(value=False)

        prepWorkFrame = ttk.Frame(optionsFrame, style="raised.TFrame")
        prepWorkFrame.pack(padx=10, pady=10, side='left')

        # --------- Missions Performed --------- #
        ttk.Label(prepWorkFrame,
        	text="Missions Complete AFTER Crew\nKidnapped, BEFORE launching\nSuicide Mission:",
        	style="raised.TLabel"
        ).grid(row=rowStart, column=colStart, padx=10, pady=5)

        ttk.Spinbox(
        	prepWorkFrame,
        	from_=0,
        	to=100,
        	textvariable=self.theCrew.missionsPrior,
        	width=10,
        	justify="center"
        ).grid(row=(rowStart+1), column=colStart, padx=10, pady=5)

        # --------- Armor Upgrade --------- #
        ttk.Label(prepWorkFrame,
        	text="Was Normandy's armor upgrded?",
        	style="raised.TLabel"
        ).grid(row=(rowStart+2), column=colStart, padx=10, pady=5)

        self.armorCheckSelect_choice = tk.StringVar(value="Yes")
        armorCheckSelect = ttk.Combobox(prepWorkFrame,
        	textvariable=self.armorCheckSelect_choice,
        	values=["Yes", "No"],
        	state="readonly"
        )
        armorCheckSelect.grid(row=(rowStart+3), column=colStart, padx=10, pady=5)

        # --------- Shield Upgrade --------- #
        ttk.Label(prepWorkFrame,
        	text="Were Normandy's Shield's upgraded?",
        	style="raised.TLabel"
        ).grid(row=(rowStart+4), column=colStart, padx=10, pady=5)

        self.shieldCheckSelect_choice = tk.StringVar(value="Yes")
        shieldCheckSelect = ttk.Combobox(prepWorkFrame,
        	textvariable=self.shieldCheckSelect_choice,
        	values=["Yes", "No"],
        	state="readonly"
        )
        shieldCheckSelect.grid(row=(rowStart+5), column=colStart, padx=10, pady=5)

        # --------- Cannon Upgrade --------- #
        ttk.Label(prepWorkFrame,
        	text="Was Normandy's main gun upgraded?",
        	style="raised.TLabel"
        ).grid(row=(rowStart+6), column=colStart, padx=10, pady=5)

        self.cannonCheckSelect_choice = tk.StringVar(value="Yes")
        cannonCheckSelect = ttk.Combobox(prepWorkFrame,
        	textvariable=self.cannonCheckSelect_choice,
        	values=["Yes", "No"],
        	state="readonly"
        )
        cannonCheckSelect.grid(row=(rowStart+7), column=colStart, padx=10, pady=5)

		# --------- Cargo Bay Squad Select --------- #
        ttk.Label(prepWorkFrame,
			text="Select Squad to Defend Cargo Bay",
			style="raised.TLabel"
		).grid(row=(rowStart+8), column=colStart, padx=10, pady=5)

        self.squadCargo1_choice = tk.StringVar(value="")
        self.squadCargo2_choice = tk.StringVar(value="")
        self.squadCargo1_selector = ttk.Combobox(prepWorkFrame,
			textvariable=self.squadCargo1_choice,
			values=self.squadCargo_names,
			state="readonly"
		)
        self.squadCargo2_selector = ttk.Combobox(prepWorkFrame,
			textvariable=self.squadCargo2_choice,
			values=self.squadCargo_names,
			state="readonly"
		)
        self.squadCargo1_selector.grid(row=(rowStart+9), column=colStart, padx=10, pady=5)
        self.squadCargo2_selector.grid(row=(rowStart+10), column=colStart, padx=10, pady=5)
        self.squadCargo1_selector.bind("<<ComboboxSelected>>", lambda event: updateSelections(self.squadCargo1_choice, self.squadCargo2_choice))
        self.squadCargo2_selector.bind("<<ComboboxSelected>>", lambda event: updateSelections(self.squadCargo2_choice, self.squadCargo1_choice))

        # --------- Go Button --------- #
        launchAttack_button = ttk.Button(prepWorkFrame, text="Launch Suicide Mission", command=self.launchAttack)
        launchAttack_button.grid(row=(rowStart+11), column=colStart, padx=10, pady=25)





        ####################################### -------- Results Frame -------- #######################################
        resultsFrame = ttk.Frame(mainFrame, style="raised.TFrame")
        resultsFrame.pack(padx=10, pady=10)#, side='left')


        ### -------- Output box listing who died and why (after each step)-------- ###
        self.crewDied_box = scrolledtext.ScrolledText(resultsFrame, width=60, height=15, wrap=tk.WORD)
        self.crewDied_box.pack(padx=10, pady=10, side="left")
        self.crewDied_box.config(state="disabled")  # start as read‑only


        ### -------- Output box listing remaining crew (after each step)-------- ###
        self.crewRemain_box = scrolledtext.ScrolledText(resultsFrame, width=40, height=15, wrap=tk.WORD)
        self.crewRemain_box.pack(padx=10, pady=10, side="left")
        self.crewRemain_box.config(state="disabled")  # start as read‑only






    def launchAttack(self):
        if ('' == self.squadCargo1_choice.get()) or ('' ==self.squadCargo2_choice.get()):
            message = "Please select two squad members to hold the cargo hold."
        else:
            for i, name in enumerate(self.survivor_names):
                if (name == self.squadCargo1_choice.get()) or (name==self.squadCargo2_choice.get()):
                    self.survivors[name].squad.set(True)
                else:
                    self.survivors[name].squad.set(False)

            updateBoolVar(self.armorCheckSelect_choice, self.upgradeArmor)
            updateBoolVar(self.shieldCheckSelect_choice, self.upgradeShield)
            updateBoolVar(self.cannonCheckSelect_choice, self.upgradeCannon)

            survivedThisRound = copy.copy(self.survivors)

            if not self.upgradeArmor.get():
                armorCheck(survivedThisRound)
            if not self.upgradeShield.get():
                shieldCheck(survivedThisRound)
            if not self.upgradeCannon.get():
                weaponsCheck(survivedThisRound)

            survivedThisRound_list = list(survivedThisRound.keys())
            message = f"After launching an attack on the collector base, {len(survivedThisRound)} remain:\n"
            for i, name in enumerate(survivedThisRound_list):
                message += f"{i+1}) {name}\n"

        self.crewRemain_box.config(state="normal")   # allow editing
        self.crewRemain_box.delete("1.0", tk.END)    # clear previous text
        self.crewRemain_box.insert(tk.END, message)  # insert new text
        self.crewRemain_box.config(state="disabled") # make read‑only again





''' GUI NOTES

### 

MissionsBeforeAttackingBase = 0 # 6 ###
upgradeArmor = False
upgradeShield = False
upgradeCannon = False

### DogFight ###
CargoBaySquad = ["Garrus", "Tali"] # ["Kasumi", "Tali"]





### The Vents ###
VentSpecialist = "Grunt" # "Jacob"
FireTeamLeader_1 = "Miranda" # "Miranda"
VentsSquad = ["Garrus", "Tali"] # ["Zaeed", "Tali"]

### The Long Walk ###
BioticSpecialist = "Miranda" # "Miranda"
FireTeamLeader_2 = "Jacob" # "Mordin"
LongWalkSquad = ["Garrus", "Tali"] # ["Zaeed", "Tali"]

### The Crew, the Final Boss, and Holding the Line
Escort = "None"
FinalFightSquad = ["Miranda", "Morinth"] # ["Morinth", "Miranda"]

'''




'''------------------------------------------------------------------------------------------
'''
if stinger:
	print()
	print("\nOkay. 3, 2, 1, let's jam! \n".center(152, "-"))
	print()

'''--------------------MAIN-------------------MAIN-------------------MAIN--------------------
'''
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()









'''------------------------------------------------------------------------------------------
'''
if stinger:
	print()
	print("\nSee you, Space Cowboy...\n".center(150, "-"))
	print()
'''------------------------------------------------------------------------------------------
'''