import sys
import re
import numpy as np


'''----------------------------------------Flags and Options----------------------------------------
'''
stinger = True 	# The just adds a Cowboy Bebop reference to the terminal run. It doesn't affect the other code and it's here for my amusement.

### Whole Crew is: ["Mordin", "Tali", "Kasumi", "Jack", "Miranda", "Jacob", "Garrus", "Samara", "Morinth", "Legion", "Thane", "Zaeed", "Grunt"]

### Before Going Through the Relay ###
notRecruited = ["Zaeed", "Kasumi"] 			# Comma seperated list (like "whole crew" above)
MissionsBeforeAttackingBase = 0 			# integer
SamaraOrMorinth = "Morinth" 				# fill in with "Samara" or "Morinth" ONLY
loyalCrew = [] 								# Comma seperated list (like "whole crew" above)
upgradeArmor = False 						# True or False
upgradeShield = False						# True or False
upgradeCannon = False						# True or False

### DogFight ###
CargoBaySquad = ["Garrus", "Tali"] 			# Comma seperated list of TWO ONLY (similar to "whole crew" above)

### The Vents ###
VentSpecialist = "Grunt" 					# Single name in quotes
FireTeamLeader_1 = "Miranda" 				# Single name in quotes
VentsSquad = ["Garrus", "Tali"] 			# Comma seperated list of TWO ONLY (similar to "whole crew" above)

### The Long Walk ###
BioticSpecialist = "Miranda" 				# Single name in quotes
FireTeamLeader_2 = "Jacob" 					# Single name in quotes
LongWalkSquad = ["Garrus", "Tali"] 			# Comma seperated list of TWO ONLY (similar to "whole crew" above)

### The Crew, the Final Boss, and Holding the Line
Escort = "None"								# Single name in quotes
FinalFightSquad = ["Miranda", "Morinth"] 	# Comma seperated list of TWO ONLY (similar to "whole crew" above)


'''
Everyone Dies Playthrough:

Don't activate Legion of Grunt
Cargo bay: 		Take Kasumi and Tali
Leader1:		Doesn't Matter
Vents:			Jacob
Leader2:		Not Miranda, Zaeed, Morinth
Squad 2:		Zaeed and either Kasumi or Tali
Biotics:		Miranda
Final Fight:	Miranda and Morinth

Only Morinth and Zaeed survive. Shoot Zaeed during his loyalty mission, Morinth pisses off during ME3
'''



'''----------------------------------------Functions and Classes----------------------------------------
'''
class Character:
	"""A ME2 Squadmate's Character Details"""
	def __init__(self, tier, loyal=False, vent=False, biotic=False, leader=False, squad=False):
		self.loyal = loyal
		self.vent = vent
		self.biotic = biotic
		self.leader = leader
		self.squad = squad
		self.tier = tier

class Crew:
	"""The Status of the Crew"""
	def __init__(self, statusKnown=False, Dr=True, percent=100):
		self.statusKnown = statusKnown
		self.Dr = Dr
		self.percent = percent

def report(d, event, crew):
	"""
	Purpose: Iterative status of the crew at any point in Suicide mission

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs
		event (str) - The next event in the Suicide Mission
		crew (Crew() class) - The status object for hte crew

	Return: N/A
	"""	
	print(f"Leading into {event}:")
	for name, char in d.items():
		char.squad = False
		print(f"\t{name}")
	print(f"\t\t{len(d)} squadmates remaining.")
	if crew.statusKnown == False:
		print(f"\t\tThe status of the crew is unknown . . . ")
	elif not crew.Dr:
		print(f"\t\tDoctor Chakwas and the crew are dead.")
	else:
		print(f"\t\tDr. Chakwas and {crew.percent}% of the crew survive.")
	print()

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
		if (v in d) and (d[v].squad == False):
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
		if (v in d) and (d[v].squad == False):
			del d[v]
			break

def ventCheck(d, leader, spec):
	"""
	Purpose: Kill the vent specialist if you choose the wrong tech specialist or leader

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs
		leader (str) - Name of the fire team leader
		spec (str) - name of the tech specialist

	Return: N/A
	"""	
	if (d[spec].vent == False) or (d[spec].loyal == False) or (d[leader].leader == False) or (d[leader].loyal == False):
		del d[spec] 
	
def bioticCheck(d, spec):
	"""
	Purpose: Kill a squad member if you choose the wrong biotic specialist

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs
		leader (str) - Name of the fire team leader
		spec (str) - name of the biotic specialist

	Return: N/A
	"""	
	if (d[spec].biotic == False) or (d[spec].loyal == False):
		l = ["Thane", "Jack", "Garrus", "Legion", "Grunt", "Samara", "Jacob", "Mordin", "Tali", "Kasumi", "Zaeed", "Morinth"]
		for i, name in enumerate(l):
			if (name in d) and (d[name].squad == True):
				del d[name]
				break

def secondLeaderCheck(d, leader):
	"""
	Purpose: Kill the fire team leader if you choose the wrong leader

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs
		leader (str) - Name of the fire team leader

	Return: N/A
	"""	
	if (leader != "Miranda") or (d[leader].leader == False) or (d[leader].loyal == False):
		del d[leader]

def get_em(d, l):
	"""
	Purpose: Kill a crew member holding the line

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs
		l (list) - The order to kill people in

	Return: N/A
	"""
	jobDone = False
	for i, v in enumerate(l):
		if (v in d) and (d[v].squad == False) and (d[v].loyal == False):
			del d[v]
			jobDone = True
			break
	if not jobDone:
		for i, v in enumerate(l):
			if (v in d) and (d[v].squad == False) and (d[v].loyal == True):
				del d[v]
				jobDone = True
				break

def holdTheLine(d):
	"""
	Purpose: Calculate survivors from from the group holding the line

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs

	Return: N/A
	"""	
	l = ["Mordin", "Tali", "Kasumi", "Jack", "Miranda", "Jacob", "Garrus", "Samara", "Morinth", "Legion", "Thane", "Zaeed", "Grunt"]
	score = 0
	people = 0
	for name, deets in d.items():
		if (deets.squad == False):
			people += 1
			score += deets.tier + int(deets.loyal)
	score /= people
	if people == 1:
		if score < 2:
			get_em(d, l)
	elif people == 2:
		if score == 0:
			get_em(d, l)
		if score < 2:
			get_em(d, l)
	elif people == 3:
		if score == 0:
			get_em(d, l)
		if score < 1:
			get_em(d, l)
		if score < 2:
			get_em(d, l)
	elif people == 4:
		if score == 0:
			get_em(d, l)
		if score < 0.5:
			get_em(d, l)
		if score <= 1:
			get_em(d, l)
		if score < 2:
			get_em(d, l)
	else:
		if score < 0.5:
			get_em(d, l)
		if score < 1.5:
			get_em(d, l)
		if score < 2:
			get_em(d, l)

def finalFight(d):
	"""
	Purpose: Calculate which squadmates survive the final showdown

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs

	Return: N/A
	"""	
	dead = []
	for name, deets in d.items():
		if (deets.squad == True) and (deets.loyal == False):
			dead.append(name)
	for i, name in enumerate(dead):
		del d[name]

def finalReport(d, c, e, e_loyal):
	"""
	Purpose: Summarize the mission.

	Args:
		d (dict) - {"name of crew member" : Character() class} pairs
		c (Crew class) - The status of the crew
		e (str) - The name of the escort
		e_loyal (bool) - Whether the escort was loyal

	Return: N/A
	"""	
	if e_loyal:
		d[e] = Character(tier=0)
	keys = list(d.keys())
	s = ""
	if len(d) == 0:
		s += f"Your entire squad perished."
	if len(d) == 1:
		s += f"Only 1 squadmate survived: {keys[0]}.\n"
	elif len(d) >= 2:
		s += f"Shepard as well as {len(d)} squadmates survive:\n"
		s += f"{keys[0]}"
		for i in range(1, len(keys)-1):
			s += f", {keys[i]}"
		if len(keys) == 2:
			s += f" and {keys[len(keys)-1]}.\n"
		else:
			s += f", and {keys[len(keys)-1]}.\n"
	if c.Dr:
		s += "Dr. Chakwas"
		if c.percent > 0:
			s += f" and {c.percent}% of the crew survive."
		else:
			s += " survives."
	if (c.percent == 0) or (c.Dr == False):
		s += "Unfortunately, the rest of your crew did not survive."
	print(f"\n{s}")



'''------------------------------------------------------------------------------------------
'''
if stinger:
	print()
	print("\nOkay. 3, 2, 1, let's jam! \n".center(152, "-"))
	print()

'''--------------------MAIN-------------------MAIN-------------------MAIN--------------------
'''

survivors = {"Grunt":Character(tier=3), "Zaeed":Character(tier=3), "Thane":Character(tier=1), "Legion":Character(vent=True, tier=1), "Samara":Character(biotic=True, tier=1), "Morinth":Character(biotic=True, tier=1), "Garrus":Character(leader=True, tier=3), "Jacob":Character(leader=True, tier=1), "Miranda":Character(leader=True, tier=1), "Jack":Character(biotic=True, tier=0), "Kasumi":Character(vent=True, tier=0), "Tali":Character(vent=True, tier=0), "Mordin":Character(tier=0)}
crewStatus = Crew()




### Before Going Through the Relay ###
notRecruited = ["Zaeed", "Kasumi"] # ["Grunt", "Legion"] ###
MissionsBeforeAttackingBase = 0 # 6 ###
SamaraOrMorinth = "Morinth" # "Morinth" ###
loyalCrew = [] # ["Mordin", "Tali", "Kasumi", "Jack", "Miranda", "Jacob", "Garrus", "Samara", "Morinth", "Legion", "Thane", "Zaeed", "Grunt"]
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








### Reconcile Crew List and Loyalty
for i, name in enumerate(loyalCrew):
	if name in survivors:
		survivors[name].loyal = True

for i, name in enumerate(notRecruited):
	del survivors[name]

if ("Morinth" in survivors) and (SamaraOrMorinth == "Morinth"):
	survivors["Morinth"].loyal = True
	if "Samara" in survivors:
		del survivors["Samara"]
if ("Samara" in survivors) and (SamaraOrMorinth == "Samara"):
	if "Morinth" in survivors:
		del survivors["Morinth"]


### Cargo Bay - Squad Selection
report(survivors, "Cargo Bay Battle", crewStatus)
for i, name in enumerate(CargoBaySquad):
	survivors[name].squad = True
if not upgradeArmor:
	armorCheck(survivors)
if not upgradeShield:
	shieldCheck(survivors)
if not upgradeCannon:
	weaponsCheck(survivors)







### Vents - Squad and Specialist Selections
report(survivors, "Vents", crewStatus)
leader = FireTeamLeader_1
spec = VentSpecialist
for i, name in enumerate(VentsSquad):
	survivors[name].squad = True
ventCheck(survivors, leader, spec)


### Long Walk - Squad and Specialist Selections
report(survivors, "Long Walk", crewStatus)
leader = FireTeamLeader_2
spec = BioticSpecialist
for i, name in enumerate(LongWalkSquad):
	survivors[name].squad = True
bioticCheck(survivors, spec)
secondLeaderCheck(survivors, leader)


## The Crew
crewStatus.statusKnown = True
escortLoyal = False
if MissionsBeforeAttackingBase > 3:
	crewStatus.percent = 0
elif MissionsBeforeAttackingBase > 0:
	crewStatus.percent = 50
if Escort not in survivors:
	crewStatus.Dr = False
else:
	escortLoyal = survivors[Escort].loyal
	del survivors[Escort]


## Final Fight - Squad Selection
report(survivors, "Final Battle", crewStatus)
for i, name in enumerate(FinalFightSquad):
	survivors[name].squad = True
holdTheLine(survivors)
finalFight(survivors)

report(survivors, "Race to the Normandy", crewStatus)
finalReport(survivors, crewStatus, Escort, escortLoyal)

'''------------------------------------------------------------------------------------------
'''
if stinger:
	print()
	print("\nSee you, Space Cowboy...\n".center(150, "-"))
	print()
'''------------------------------------------------------------------------------------------
'''