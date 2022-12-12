import PySimpleGUI as sg
import numpy as np
import traceback # https://stackoverflow.com/questions/3702675/how-to-catch-and-print-the-full-exception-traceback-without-halting-exiting-the


sg.Window.get_screen_size() # https://github.com/PySimpleGUI/PySimpleGUI/issues/1996
w, h = sg.Window.get_screen_size()

random_theme = np.random.choice(sg.theme_list())
random_theme = np.random.choice([k for k in sg.theme_list() if "Mono" in k])
random_theme = "BlueMono"


sg.theme(random_theme)

def name2dictionary(name, all_gear):
    #
    # Given an item name ("Adhemar Bonnet +1A"), find the dictionary (adhemar_bonnet_A) which containts that item's stats.
    # This will be used often, may as well make it a function, even if it is inefficient.
    # First check Name2, then check Name. This is so you don't mix up different augment paths.
    # Name is mostly for finding the icon anyway.
    #
    for i,k in enumerate(all_gear):
        gear_name = k["Name2"] if "Name2" in k else k["Name"]
        if name == gear_name:
            return(all_gear[i])
    return(Empty)

from tab_inputs import * # Load the inputs tab
from tab_select_gear import *  # Load the select_gear tab
from tab_outputs import * # Load the outputs tab.

# Add a menu bar for the user to adjust font size and stuff.
font_size_options = [f"&{k:>3d}::font{k}" for k in [l for l in range(6,16)]]
# https://csveda.com/python-menu-button-menu-and-option-menu-with-pysimplegui/
menu_def=[['&Edit', ['&Font Size',font_size_options, '&Theme','---', '!&Save Defaults']]]

layout = [
          [
          [sg.Menu(menu_def, font='Verdana', pad=(10,10),key="menubar_select")],
          sg.TabGroup([
                        [
                         sg.Tab("Inputs", input_tab),
                         sg.Tab("Select Gear", select_gear_tab),
                         sg.Tab("Outputs", ws_tab),
                         ]
                       ],key="tab group")
          ]
         ]

# window_styles = ["default", "winnative", "clam", "alt", "classic", "vista", "xpnative"] # https://old.reddit.com/r/learnpython/comments/k0m9on/how_can_i_change_the_ui_style_in_pysimplegui/
window_styles = ["default", "alt"] # https://old.reddit.com/r/learnpython/comments/k0m9on/how_can_i_change_the_ui_style_in_pysimplegui/
random_style = np.random.choice(window_styles)
random_style = "default"

window = sg.Window(f"Kastra WS Damage Simulator (2022 December 12) - Theme:{random_theme} - Style:{random_style}",layout,size=(700,900),resizable=True,alpha_channel=1.0,finalize=True,no_titlebar=False,ttk_theme=random_style)
# window["main start radio NIN"].update(visible=True)


while True:
    # Run the code within this while True block once.
    # Then wait for the user to perform an event before running another loop.
    main_jobs = sorted(["NIN", "DRK", "SCH", "RDM", "BLM", "SAM", "DRG", "WHM", "WAR", "COR", "BRD", "THF","MNK"]) # If you add jobs here, make sure to add them in the tab_inputs.py file too.


    ws_dict = {"Katana": ["Blade: Chi", "Blade: Hi", "Blade: Kamu", "Blade: Metsu", "Blade: Shun", "Blade: Ten", "Blade: Ku", "Blade: Ei", "Blade: Yu",],
                "Great Katana": ["Tachi: Rana", "Tachi: Fudo", "Tachi: Kaiten", "Tachi: Shoha", "Tachi: Kasha", "Tachi: Gekko", "Tachi: Jinpu",],
                "Dagger": ["Evisceration", "Exenterator", "Mercy Stroke", "Aeolian Edge", "Rudra's Storm", "Shark Bite", "Dancing Edge", "Mordant Rime","Mandalic Stab",],
                "Sword": ["Savage Blade", "Expiacion", "Death Blossom", "Chant du Cygne", "Knights of Round", "Sanguine Blade", "Seraph Blade","Red Lotus Blade"],
                "Scythe": ["Insurgency", "Cross Reaper", "Entropy", "Quietus", "Catastrophe","Infernal Scythe","Shadow of Death","Dark Harvest","Spiral Hell"],
                "Great Sword":["Torcleaver","Scourge","Resolution","Freezebite", "Herculean Slash",],
                "Club":["Hexa Strike","Realmrazer","Seraph Strike","Randgrith","Black Halo","Judgment"],
                "Polearm":["Stardiver", "Impulse Drive", "Penta Thrust", "Geirskogul", "Drakesbane", "Camlann's Torment","Raiden Thrust","Thunder Thrust"],
                "Staff":["Cataclysm","Shattersoul","Earth Crusher","Vidohunir","Retribution",],
                "Great Axe":["Ukko's Fury", "Upheaval", "Metatron Torment", "King's Justice",],
                "Axe":["Cloudsplitter","Ruinator","Decimation","Rampage","Primal Rend",],
                "Archery":["Empyreal Arrow", "Flaming Arrow", "Namas Arrow",],
                "Marksmanship":["Last Stand","Hot Shot","Leaden Salute","Wildfire"],
                "Hand-to-Hand":["Raging Fists","Howling Fist","Dragon Kick","Asuran Fists","Tornado Kick","Shijin Spiral","Final Heaven","Victory Smite","Ascetic's Fury",]}

    # Read the window. Record the action that triggered the window to refresh as well as the key-value pairs associated with all variables throughout the window.
    event, values = window.read()
    # print(event)
    # Exit the program if given exit or null command.
    if event in (None, "Exit"):
        break

    # # Allow the user to define their font size (lazy way of having the user try to fix their own UI formatting issues). Currently broken. Can't find a way to update all text programmatically yet
    if event[1:] in [k[2:] for k in font_size_options]:
        # This is not well-written yet. Some GUI elements do not have a font keyword in their .update() method.
        # Input.update() was just recently updated to include it, but Button (and others) are missing it still.
        # To update the font of elements missing the font keyword, I'm using the code from jason990420 (https://github.com/PySimpleGUI/PySimpleGUI/issues/6012)
        # It works, but there may be stuff that breaks because of it.
        new_size = event.strip().split("::")[0]
        new_font = ["Cascadia Mono", new_size]
        for value in values:
            if window[value].Font == ['Cascadia Mono', 9]:
                try:
                    window[value].update(font=new_font)
                except:
                    window[value].Widget.configure(font=new_font)    # state is 'normal', 'readonly' or 'disabled'

    try:
        # If the user selects a new enemy from the enemy drop down list, then automatically update the enemy stats.
        if event == "enemy_name":
            enemy = values["enemy_name"]
            if enemy == "Custom":
                window["enemy_location"].update("")
            else:
                window["enemy_level"].update(f"{preset_enemies[enemy]['Level']}")
                window["enemy_evasion"].update(f"{preset_enemies[enemy]['Evasion']}")
                window["enemy_defense"].update(f"{preset_enemies[enemy]['Defense']}")
                window["enemy_mdefense"].update(f"{preset_enemies[enemy]['Magic Defense']}")
                window["enemy_vit"].update(f"{preset_enemies[enemy]['VIT']}")
                window["enemy_agi"].update(f"{preset_enemies[enemy]['AGI']}")
                window["enemy_int"].update(f"{preset_enemies[enemy]['INT']}")
                window["enemy_location"].update(f"({preset_enemies[enemy]['Location']})")



        # Update the drop down menus for BRD songs when the user selects a song that is already selected somewhere else.
        if event in ["song1","song2","song3","song4"]:
            songs = {"song1":values["song1"], "song2":values["song2"], "song3":values["song3"], "song4":values["song4"]}
            song1 = values["song1"]
            song2 = values["song2"]
            song3 = values["song3"]
            song4 = values["song4"]
            i = int(event[-1])
            for j in [k+1 for k in range(4) if (k+1)!=i]:
                if songs[f"song{i}"] == songs[f"song{j}"]:
                    window[f"song{j}"].update(value="None")

        # Update the drop down menus for COR rolls when the user selects a roll that is already selected in the other slot.
        if event in ["roll1","roll2"]:
            rolls = {"roll1":values["roll1"], "roll2":values["roll2"]}
            roll1 = values["roll1"]
            roll2 = values["roll2"]
            i = int(event[-1])
            for j in [k+1 for k in range(2) if (k+1)!=i]:
                if rolls[f"roll{i}"] == rolls[f"roll{j}"]:
                    window[f"roll{j}"].update(value="None")

        # Update the drop down menus for GEO entrusts when the user selects an entrust bubble that is already selected as an indi- or geo-bubble.
        if event in ["entrust","indibuff","geobuff"]:
            indibubble = values["indibuff"].split("-")[-1]
            geobubble = values["geobuff"].split("-")[-1]
            entrustbubble = values["entrust"].split("-")[-1]
            if (entrustbubble == indibubble) or (entrustbubble == geobubble):
                window["entrust"].update(value="None")

            if event == "indibuff":
                if indibubble == geobubble:
                    window["geobuff"].update(value="None")
            if event == "geobuff":
                if geobubble == indibubble:
                    window["indibuff"].update(value="None")



        # Unlock Light Shot if COR is selected.
        if event == "cor_on":
            if values["cor_on"]:
                window["LIGHTSHOT"].update(disabled=False)
                window["Crooked Cards"].update(disabled=False)
            else:
                window["LIGHTSHOT"].update(False)
                window["LIGHTSHOT"].update(disabled=True)
                window["Crooked Cards"].update(False)
                window["Crooked Cards"].update(disabled=True)

        # Unlock Bolster and Blaze of Glory if GEO is selected.
        if event == "geo_on":
            if values["geo_on"]:
                window["bolster"].update(disabled=False)
                window["geo_bog"].update(disabled=False)
            else:
                window["bolster"].update(False)
                window["bolster"].update(disabled=True)
                window["geo_bog"].update(False)
                window["geo_bog"].update(disabled=True)

        # Automatically turn off and disable Blaze of Glory if Bolster is turned on.
        if event == "bolster":
            if values["bolster"]:
                if values["geo_bog"]:
                    window["geo_bog"].update(False)
                window["geo_bog"].update(disabled=True)
            else:
                window["geo_bog"].update(disabled=False)

        # Unlock Soul Voice if BRD is selected.
        if event == "brd_on":
            if values["brd_on"]:
                window["soulvoice"].update(disabled=False)
                window["marcato"].update(disabled=False)
            else:
                window["soulvoice"].update(False)
                window["soulvoice"].update(disabled=True)
                window["marcato"].update(False)
                window["marcato"].update(disabled=True)

        # Automatically turn off Marcato if Soul Voice is turned on.
        if event == "soulvoice":
            if values["soulvoice"]:
                if values["marcato"]:
                    window["marcato"].update(False)
                window["marcato"].update(disabled=True)
            else:
                window["marcato"].update(disabled=False)

        # Setup the buttons which display/hide gear lists on the gear tab.
        if event.split()[0] == "display":
            slot = event.split()[1] # The slot selected by the user
            main_job = values["mainjob"] # The main job from the inputs tab
            for k in ["main","sub","ranged","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                for l in main_jobs:
                    if slot==k and main_job == l:
                        window[f"{k} display {l}"].update(visible=True)
                    else:
                        window[f"{k} display {l}"].update(visible=False)

        # Setup buttons to automatically select everything in the displayed list.
        if event == "select all gear":
            main_job = values["mainjob"]
            for k in ["main","sub","ranged","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                if window[f"{k} display {main_job}"].visible:
                    slot = k
                    break
            for k in values:
                if type(k) == str:
                    if k.split()[0][:-1] == slot:
                        if k.split(";;")[-1] == main_job:
                            window[k].update(True)
                        else:
                            window[k].update(False)
                        

        # Setup buttons to automatically unselect everything in the displayed list.
        if event == "unselect all gear":
            main_job = values["mainjob"]
            for k in ["main","sub","ranged","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                if window[f"{k} display {main_job}"].visible:
                    slot = k
                    break
            for k in values:
                if type(k) == str:
                    if k.split()[0][:-1] == slot and k.split(";;")[-1] == main_job:
                        window[k].update(False)

        # select every piece of equipment in all slots that your main job can equip.
        if event == "select ALL main":
            gear_map = {"main":mains, # Map the slot name to the list of gear to be considered in that slot.
                        "sub":subs + grips,
                        "ranged":ranged,
                        "ammo":ammos,
                        "head":heads,
                        "neck":necks,
                        "ear1":ears,
                        "ear2":ears2,
                        "body":bodies,
                        "hands":hands,
                        "ring1":rings,
                        "ring2":rings2,
                        "back":capes,
                        "waist":waists,
                        "legs":legs,
                        "feet":feet}
            main_job = values["mainjob"]
            ws_name = values["select weaponskill"]

            for slot in ["main","sub","ranged","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                for job in main_jobs: # So we can turn off all other job gear.
                    displayed_equipment_list = gear_map[slot] # List of ALL gear in each slot
                    for k in values: # values is the dictionary of stuff saved in the GUI.
                        if type(k) == str: # Some of the keys are integers?? skip them here
                            if k.split()[0][:-1] == slot: # sub:  ammo:  main:  etc
                                for l in displayed_equipment_list:
                                    if job.lower() in l["Jobs"] and main_job==job:
                                        window[f"{slot}: {l['Name2']};;{job}"].update(True) # Turn on all versions of item checkboxes that correspond to your main job (Heishi Shorinken R15;;NIN)

                                        # If you're using a melee weapon skill, then unselect all main weapons that can't use your selected weapon skill.
                                        if ws_name not in ws_dict["Marksmanship"]+ws_dict["Archery"]: # If you're testing a melee WS
                                            if slot == "main" and ws_name not in ws_dict[l["Skill Type"]]: # Unselect main weapons that can't use the selected weapon skill
                                                window[f"{slot}: {l['Name2']};;{job}"].update(False)
                                            if slot == "ranged" and l.get("Type","None") in ["Bow", "Gun"]: # Do not test ranged weapons with melee WSs (TP Bonus Gun??)
                                                if job not in ["COR","RNG"]:
                                                    window[f"{slot}: {l['Name2']};;{job}"].update(False)
                                        # Now, if you're using a ranged weapon skill, then unselect all ranged weapons that can't use your selected weapon skill, but do select all main weapons still.
                                        else: # Else you're testing a ranged WS
                                            if slot == "ranged" and ws_name not in ws_dict.get(l.get("Skill Type","None"),[]): # Turn off guns for bow weapon skills and bows for gun weapon skills
                                                window[f"{slot}: {l['Name2']};;{job}"].update(False)
                                            if slot == "ammo" and l.get("Type","None") not in ["Bullet", "Arrow"]: # Do not test ranged weapons with equipment ammos. You can't shoot a seething bomblet
                                                window[f"{slot}: {l['Name2']};;{job}"].update(False)
                                    else:
                                        if f"{slot}: {l['Name2']};;{job}" in window.AllKeysDict: # https://github.com/PySimpleGUI/PySimpleGUI/issues/1597
                                            window[f"{slot}: {l['Name2']};;{job}"].update(False) # Turn off all versions of item checkboxes corresponding to not your main job (Heishi Shorinken R15;;DRK)


        # Setup buttons to show/hide radio buttons on the starting gearset tab.
        # Clicking the "main" slot will show the radio buttons for the "main" gear on the right while hiding all other slot radio buttons
        # Modified to only show gear that your main job can use.
        if event.split()[0] == "showstart":
            main_job = values["mainjob"]
            slot = event.split()[-1]
            if slot == "---":
                continue
            for k in ["main","sub","ranged","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                for l in main_jobs:
                    if k == slot:
                        if l == main_job:
                            if not window[f"{k} start radio {l}"].visible:
                                window[f"{k} start radio {l}"].update(visible=True)
                        elif window[f"{k} start radio {l}"].visible:
                            window[f"{k} start radio {l}"].update(visible=False)
                    else:
                        if window[f"{k} start radio {l}"].visible:
                            window[f"{k} start radio {l}"].update(visible=False)

        if event == "subjob":
            main_job = values["mainjob"]
            sub_job = values["subjob"]
            if sub_job == main_job:
                window["subjob"].update("None") # Prioritize main job if main and sub are set to the same thing.

        # Update the radio list if the main job changes.
        if event == "mainjob":
            main_job = values["mainjob"]
            sub_job = values["subjob"]
           
            if sub_job == main_job:
                window["subjob"].update("None") # Prioritize main job if main and sub are set to the same thing.

            spell_dict = { # This SHOULD be a copy/paste of the spell_dict in tab_inputs.py
              "NIN":["Doton: Ichi","Doton: Ni","Doton: San","Suiton: Ichi","Suiton: Ni","Suiton: San","Huton: Ichi","Huton: Ni","Huton: San","Katon: Ichi","Katon: Ni","Katon: San","Hyoton: Ichi","Hyoton: Ni","Hyoton: San", "Raiton: Ichi","Raiton: Ni","Raiton: San",],
              "BLM":["Stone","Stone II","Stone III","Stone IV","Stone V","Stone VI","Stoneja",
                     "Water","Water II","Water III","Water IV","Water V","Water VI","Waterja",
                     "Aero","Aero II","Aero III","Aero IV","Aero V","Aero VI","Aeroja",
                     "Fire","Fire II","Fire III","Fire IV","Fire V","Fire VI","Firaja",
                     "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V","Blizzard VI","Blizzaja",
                     "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V","Thundaja"],
              "RDM":["Stone","Stone II","Stone III","Stone IV","Stone V",
                     "Water","Water II","Water III","Water IV","Water V",
                     "Aero","Aero II","Aero III","Aero IV","Aero V",
                     "Fire","Fire II","Fire III","Fire IV","Fire V",
                     "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V",
                     "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V",],
              "SCH":["Stone","Stone II","Stone III","Stone IV","Stone V","Geohelix II",
                     "Water","Water II","Water III","Water IV","Water V","Hydrohelix II",
                     "Aero","Aero II","Aero III","Aero IV","Aero V","Anemohelix II",
                     "Fire","Fire II","Fire III","Fire IV","Fire V","Pyrohelix",
                     "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V","Cryohelix II",
                     "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V","Ionohelix II",
                     "Luminohelix II", "Noctohelix II"],
              "DRK":["Stone","Stone II","Stone III",
                     "Water","Water II","Water III",
                     "Aero","Aero II","Aero III",
                     "Fire","Fire II","Fire III",
                     "Blizzard","Blizzard II","Blizzard III",
                     "Thunder","Thunder II","Thunder III"],
              "COR":["Earth Shot", "Water Shot", "Wind Shot", "Fire Shot", "Ice Shot", "Thunder Shot"]
            }
            
            # Show/hide checkboxes based on main job selected
            if main_job == "NIN": # Show Futae for NIN main
                window["futae toggle"].update(visible=True) # Show Futae
                window["futae toggle"].update(False) # Make sure it's reset to False
                window["magic burst toggle"].update(visible=True) # Show Magic Burst
                window["magic burst toggle"].update(False) # Make sure it's reset to False
            else:
                window["futae toggle"].update(visible=False) # Not NIN? Hide Futae
                window["futae toggle"].update(False) # Disable Futae if not NIN so it's hidden and disabled.

            if main_job == "SCH": # Enable Ebullience for SCH main
                window["ebullience toggle"].update(visible=True)
                window["ebullience toggle"].update(False)
                window["magic burst toggle"].update(visible=True)
                window["magic burst toggle"].update(False)
            else:
                window["ebullience toggle"].update(visible=False)
                window["ebullience toggle"].update(False)

            if main_job == "THF": # Enable SA/TA for THF main
                window["sa toggle"].update(visible=True)
                window["sa toggle"].update(False)
                window["ta toggle"].update(visible=True)
                window["ta toggle"].update(False)
            else:
                window["sa toggle"].update(visible=False)
                window["sa toggle"].update(False)
                window["ta toggle"].update(visible=False)
                window["ta toggle"].update(False)

            if main_job == "MNK": # Enable Impetus/Footwork for MNK main
                window["footwork toggle"].update(visible=True)
                window["footwork toggle"].update(False)
                window["impetus toggle"].update(visible=True)
                window["impetus toggle"].update(False)
            else:
                window["footwork toggle"].update(visible=False)
                window["footwork toggle"].update(False)
                window["impetus toggle"].update(visible=False)
                window["impetus toggle"].update(False)

            # Hide the magic burst button if not on one of the nuking jobs.
            if main_job not in ["NIN","SCH","BLM","WHM","RDM","GEO","DRK"]:
                window["magic burst toggle"].update(visible=False)
                window["magic burst toggle"].update(False)


            if main_job in spell_dict: # Enable magic sets for casting jobs.
                window["select spell"].update(values=spell_dict[main_job])
                window["select spell"].update(spell_dict[main_job][0])
                window["quicklook magic"].update(disabled=False)
                window["Run Magic"].update(disabled=False)
            else:
                window["quicklook magic"].update(disabled=True)
                window["Run Magic"].update(disabled=True)
                window["select spell"].update(values=[])





            gear_map = {"main":mains, # Map the slot name to the list of gear to be considered in that slot.
                        "sub":subs + grips,
                        "ranged":ranged,
                        "ammo":ammos,
                        "head":heads,
                        "neck":necks,
                        "ear1":ears,
                        "ear2":ears2,
                        "body":bodies,
                        "hands":hands,
                        "ring1":rings,
                        "ring2":rings2,
                        "back":capes,
                        "waist":waists,
                        "legs":legs,
                        "feet":feet}

            # Update the radio and checkbox lists to display only items the main job can equip
            for k in ["main","sub","ranged","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                for job in main_jobs:
                    if window[f"{k} start radio {job}"].visible:
                        slot = k
                    window[f"{k} start radio {job}"].update(visible=False)
                    window[f"{k} display {job}"].update(visible=False)

                    displayed_equipment_list = gear_map[k] # Start checkbox part (copy pasted from select ALL)
                    for k2 in values:
                        if type(k2) == str:
                            if k2.split()[0][:-1] == k: # sub:  ammo:  main:  etc
                                for l in displayed_equipment_list:
                                    if f"{k}: {l['Name2']};;{job}" in window.AllKeysDict: # https://github.com/PySimpleGUI/PySimpleGUI/issues/1597
                                        window[f"{k}: {l['Name2']};;{job}"].update(False)

            window[f"{slot} start radio {main_job}"].update(visible=True)
            window[f"{slot} display {main_job}"].update(visible=True)
        

        # Setup fancy pictures on the buttons when you select a radio button on starting set tab.
        # The pictures and the WS list will update based on your selection.
        if event[:5] == "start":
            # First update the gear picture:
            slot = event.split(":")[0][5:]
            item = event.split(":")[1].split(";;")[0][1:] # Had to append "NIN" to the end of the NIN list to distinguish it from the DRK, BLM, etc lists. I simply remove that bit here or it'll say something like "Heishi Shorinken R15;;NIN" and yell at us
            item_name = all_names_map[item]
            window[f"showstart {slot}"].update(image_data=item2image(item_name))
            window[f"showstart {slot}"].set_tooltip(item)

            # Now update the WS list:
            if slot in ["main","ranged"]:
                skill_type_main0 = starting_gearset["main"].get("Skill Type","None")
                skill_type_ranged0 = starting_gearset["ranged"].get("Skill Type","None")

                item_dictionary = name2dictionary(item, all_gear)
                starting_gearset[slot] = item_dictionary

                skill_type_main = starting_gearset["main"].get("Skill Type","None") # None is possible in a weird edge case the user has to be trying to make happen.
                main_ws_list = ws_dict.get(skill_type_main,[])
                # print(skill_type_main, starting_gearset)

                skill_type_ranged = starting_gearset["ranged"].get("Skill Type","None") # Ranged skill type might be "Instrument"
                ranged_ws_list = ws_dict.get(skill_type_ranged,[])

                if (slot=="ranged" and (skill_type_ranged0 != skill_type_ranged)) or (slot=="main" and (skill_type_main0 != skill_type_main)):

                    updated_ws_list = sorted(main_ws_list + ranged_ws_list)
                    # print(skill_type_main,skill_type_ranged)

                    window["select weaponskill"].update(values=updated_ws_list)
                    window["select weaponskill"].update(updated_ws_list[0])


        # Begin collecting variables to pass into the main code. There will be a lot of variables.
        if event in ["Run WS", "Run Magic", "quicklook", "quicklook magic", "quicklook tp", "get stats"]:
            
            main_job = values["mainjob"]
            sub_job = values["subjob"]


            # Define weapon skill and TP range.
            ws_name = values["select weaponskill"]
            min_tp = int(values["mintp"])
            max_tp = int(values["maxtp"])


            # New window to show output?
            # window2 = sg.Window(f"{main_job}/{sub_job}  {ws_name}  {min_tp}-{max_tp}",[[[sg.Push(),sg.Output(size=(150, 60),font=font_choice),sg.Push()]]],size=(800 ,500),resizable=True,alpha_channel=1.0,finalize=True,no_titlebar=False,ttk_theme=random_style)


            fitn = 2 # Fit two slots simultaneously. Hard-coded because 3 isn't worth the time and 1 occasionally results in incorrect sets

            # How many simulations in the final plot?
            n_sims = int(values["n_sims"]) if int(values["n_sims"]) > 100 else 100


            # How many maximum iterations before assuming converged? Currently hard-coded to 10 and 0. 0 means "do not find best set."
            n_iter = 10 if values["find set"] else 0


            # Define the starting gearset.
            for k in values:
                if type(k)==str:
                    if k[:5] == "start" and ":" in k: # If the key is a "start_____: " key for a starting item
                        if values[k]: # if the start item is set to true
                            slot = k.split(":")[0][5:] # The slot is recorded in the key
                            item_name2 = k.split(":")[1].split(";;")[0][1:] # The item name is also recorded in the key, but there is one item per job that can equip it, so we must remove the ";;NIN" bit. This is because we can't dynamically alter radio lists in PySimpleGUI...
                            starting_gearset[slot] = name2dictionary(item_name2,all_gear)


            # Define buffs
            from buffs import *

            # Define BRD buffs
            brd_on = values["brd_on"]
            active_songs = [values[k] for k in values if "song"==k[:4]]
            marcato = values["marcato"]
            soulvoice = values["soulvoice"]
            nsong = int(values["nsong"].split()[-1])

            brd_min5_attack  = ((brd["Minuet V"]["Attack"][0] + min(8,nsong)*brd["Minuet V"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet V" else 1.0) if "Minuet V" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_min4_attack  = ((brd["Minuet IV"]["Attack"][0] + min(8,nsong)*brd["Minuet IV"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet IV" else 1.0) if "Minuet IV" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_min3_attack  = ((brd["Minuet III"]["Attack"][0] + min(8,nsong)*brd["Minuet III"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet III" else 1.0) if "Minuet III" in active_songs else 0)*(1.0+1.0*soulvoice)

            brd_hm_accuracy        = ((brd["Honor March"]["Accuracy"][0] + min(8,nsong)*brd["Honor March"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_rangedaccuracy  = ((brd["Honor March"]["Ranged Accuracy"][0] + min(8,nsong)*brd["Honor March"]["Ranged Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_attack          = ((brd["Honor March"]["Attack"][0] + min(8,nsong)*brd["Honor March"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_rangedattack    = ((brd["Honor March"]["Ranged Attack"][0] + min(8,nsong)*brd["Honor March"]["Ranged Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_haste           = ((brd["Honor March"]["Haste"][0] + min(8,nsong)*brd["Honor March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)


            brd_swordmad_accuracy  = ((brd["Sword Madrigal"]["Accuracy"][0] + min(8,nsong)*brd["Sword Madrigal"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Sword Madrigal" else 1.0) if "Sword Madrigal" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_blademad_accuracy  = ((brd["Blade Madrigal"]["Accuracy"][0] + min(8,nsong)*brd["Blade Madrigal"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Blade Madrigal" else 1.0) if "Blade Madrigal" in active_songs else 0)*(1.0+1.0*soulvoice)

            brd_vmarch_haste  = ((brd["Victory March"]["Haste"][0] + min(8,nsong)*brd["Victory March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Victory March" else 1.0) if "Victory March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_amarch_haste  = ((brd["Advancing March"]["Haste"][0] + min(8,nsong)*brd["Advancing March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Advancing March" else 1.0) if "Advancing March" in active_songs else 0)*(1.0+1.0*soulvoice)


            brd_attack = brd_on*int(brd_min5_attack + brd_min4_attack + brd_min3_attack + brd_hm_attack)
            brd_accuracy = brd_on*int(brd_hm_accuracy + brd_swordmad_accuracy + brd_blademad_accuracy)
            brd_rangedaccuracy = brd_on*int(brd_hm_accuracy)
            brd_haste = brd_on*(brd_vmarch_haste + brd_amarch_haste + brd_hm_haste)


            # Define COR buffs: Total bonus stat obtained from a Lucky roll with "Rolls +nroll" bonus from gear.
            cor_on = values["cor_on"]
            active_rolls = [values["roll1"], values["roll2"]]
            nroll = int(values["nroll"].split()[-1])
            cor_sam = cor["Samurai"]["Store TP"][0] + nroll*cor["Samurai"]["Store TP"][1] if "Samurai" in active_rolls else 0
            cor_chaos = cor["Chaos"]["Attack"][0] + nroll*cor["Chaos"]["Attack"][1] if "Chaos" in active_rolls else 0
            cor_hunter = cor["Hunter"]["Accuracy"][0] + nroll*cor["Hunter"]["Accuracy"][1] if "Hunter's" in active_rolls else 0
            cor_rogue = cor["Rogue"]["Crit Rate"][0] + nroll*cor["Rogue"]["Crit Rate"][1] if "Rogue's" in active_rolls else 0
            cor_wizard = cor["Wizard"]["Magic Attack"][0] + nroll*cor["Wizard"]["Magic Attack"][1] if "Wizard's" in active_rolls else 0
            cor_fighter = cor["Fighter"]["DA"][0] + nroll*cor["Fighter"]["DA"][1] if "Fighter's" in active_rolls else 0
            crooked = values["Crooked Cards"]
            cor_stp = cor_on*cor_sam*(1.0+0.2*crooked if values["roll1"]=="Samurai" else 1.0)
            cor_attack = cor_on*cor_chaos*(1.0+0.2*crooked if values["roll1"]=="Chaos" else 1.0)
            cor_accuracy = cor_on*cor_hunter*(1.0+0.2*crooked if values["roll1"]=="Hunter's" else 1.0)
            cor_critrate = cor_on*cor_rogue*(1.0+0.2*crooked if values["roll1"]=="Rogue's" else 1.0)
            cor_magicattack = cor_on*cor_wizard*(1.0+0.2*crooked if values["roll1"]=="Wizard's" else 1.0)
            cor_da = cor_on*cor_fighter*(1.0+0.2*crooked if values["roll1"]=="Fighter's" else 1.0)


            # Define GEO buffs
            geo_on = values["geo_on"]
            nbubble = int(values["nbubble"].split()[-1])
            indibubble = values["indibuff"]
            geobubble = values["geobuff"]
            geomancy_potency = float(values["geomancy_potency"])/100
            geomancy_potency = 0 if geomancy_potency < 0 else geomancy_potency
            geomancy_potency = 1 if geomancy_potency > 1 else geomancy_potency
            active_bubbles = [indibubble.split("-")[-1],geobubble.split("-")[-1]]
            entrust = values["entrust"]
            blazeofglory = values["geo_bog"]
            bolster = values["bolster"]
            geo_attack = geo_on*((geo["Fury"]["Attack"][0] + nbubble*geo["Fury"]["Attack"][1] if "Fury" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Fury"))*(1.0+1.0*bolster) + (geo["Fury"]["Attack"][0] if entrust == "Entrust-Fury" else 0))
            geo_accuracy = geo_on*((geo["Precision"]["Accuracy"][0] + nbubble*geo["Precision"]["Accuracy"][1] if "Precision" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Precision"))*(1.0+1.0*bolster) + (geo["Precision"]["Accuracy"][0] if entrust == "Entrust-Precision" else 0))
            geo_haste = geo_on*((geo["Haste"]["Haste"][0] + nbubble*geo["Haste"]["Haste"][1] if "Haste" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Haste"))*(1.0+1.0*bolster) + (geo["Haste"]["Haste"][0] if entrust == "Entrust-Haste" else 0))
            geo_magicaccuracy = geo_on*((geo["Focus"]["Magic Accuracy"][0] + nbubble*geo["Focus"]["Magic Accuracy"][1] if "Focus" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Focus"))*(1.0+1.0*bolster) + (geo["Focus"]["Magic Accuracy"][0] if entrust == "Entrust-Focus" else 0))
            geo_magicattack = geo_on*((geo["Acumen"]["Magic Attack"][0] + nbubble*geo["Acumen"]["Magic Attack"][1] if "Acumen" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Acumen"))*(1.0+1.0*bolster) + (geo["Acumen"]["Magic Attack"][0] if entrust == "Entrust-Acumen" else 0))
            geo_str = geo_on*((geo["STR"]["STR"][0] + nbubble*geo["STR"]["STR"][1] if "STR" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-STR"))*(1.0+1.0*bolster) + (geo["STR"]["STR"][0] if entrust == "Entrust-STR" else 0))
            geo_dex = geo_on*((geo["DEX"]["DEX"][0] + nbubble*geo["DEX"]["DEX"][1] if "DEX" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-DEX"))*(1.0+1.0*bolster) + (geo["DEX"]["DEX"][0] if entrust == "Entrust-DEX" else 0))
            geo_vit = geo_on*((geo["VIT"]["VIT"][0] + nbubble*geo["VIT"]["VIT"][1] if "VIT" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-VIT"))*(1.0+1.0*bolster) + (geo["VIT"]["VIT"][0] if entrust == "Entrust-VIT" else 0))
            geo_agi = geo_on*((geo["AGI"]["AGI"][0] + nbubble*geo["AGI"]["AGI"][1] if "AGI" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-AGI"))*(1.0+1.0*bolster) + (geo["AGI"]["AGI"][0] if entrust == "Entrust-AGI" else 0))
            geo_int = geo_on*((geo["INT"]["INT"][0] + nbubble*geo["INT"]["INT"][1] if "INT" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-INT"))*(1.0+1.0*bolster) + (geo["INT"]["INT"][0] if entrust == "Entrust-INT" else 0))
            geo_mnd = geo_on*((geo["MND"]["MND"][0] + nbubble*geo["MND"]["MND"][1] if "MND" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-MND"))*(1.0+1.0*bolster) + (geo["MND"]["MND"][0] if entrust == "Entrust-MND" else 0))
            geo_chr = geo_on*((geo["CHR"]["CHR"][0] + nbubble*geo["CHR"]["CHR"][1] if "CHR" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-CHR"))*(1.0+1.0*bolster) + (geo["CHR"]["CHR"][0] if entrust == "Entrust-CHR" else 0))

            frailty_potency = (geomancy_potency)*(geo_on*((geo["Frailty"]["Defense"][0] + nbubble*geo["Frailty"]["Defense"][1] if "Frailty" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Frailty"))*(1.0+1.0*bolster) + (geo["Frailty"]["Defense"][0] if entrust == "Entrust-Frailty" else 0)))
            malaise_potency = (geomancy_potency)*(geo_on*((geo["Malaise"]["Magic Defense"][0] + nbubble*geo["Malaise"]["Magic Defense"][1] if "Malaise" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Malaise"))*(1.0+1.0*bolster) + (geo["Malaise"]["Magic Defense"][0] if entrust == "Entrust-Malaise" else 0)))
            torpor_potency = (geomancy_potency)*(geo_on*((geo["Torpor"]["Evasion"][0] + nbubble*geo["Torpor"]["Evasion"][1] if "Torpor" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Torpor"))*(1.0+1.0*bolster) + (geo["Torpor"]["Evasion"][0] if entrust == "Entrust-Torpor" else 0)))


            # Define buffs from white magic:
            whm_on = values["whm_on"]
            whm_haste = whm_on*(whm["Haste"]["Haste"]*(values["nhaste"] == "Haste") + whm["Haste II"]["Haste"]*(values["nhaste"] == "Haste II"))
            whm_str   = whm_on*(whm["Boost-STR"]["STR"]*(values["whm_boost"]=="Boost-STR"))
            whm_dex   = whm_on*(whm["Boost-DEX"]["DEX"]*(values["whm_boost"]=="Boost-DEX"))
            whm_vit   = whm_on*(whm["Boost-VIT"]["VIT"]*(values["whm_boost"]=="Boost-VIT"))
            whm_agi   = whm_on*(whm["Boost-AGI"]["AGI"]*(values["whm_boost"]=="Boost-AGI"))
            whm_int   = whm_on*(whm["Boost-INT"]["INT"]*(values["whm_boost"]=="Boost-INT"))
            whm_mnd   = whm_on*(whm["Boost-MND"]["MND"]*(values["whm_boost"]=="Boost-MND"))
            whm_chr   = whm_on*(whm["Boost-CHR"]["CHR"]*(values["whm_boost"]=="Boost-CHR"))

            # Define Dia
            dia_dictionary = {"None":0,
                              "Dia": 104./1024+(28./1024*values["LIGHTSHOT"]),
                              "Dia II": 156./1024+(28./1024*values["LIGHTSHOT"]),
                              "Dia III": 208./1024+(28./1024*values["LIGHTSHOT"]),
            }
            dia_potency = dia_dictionary[values["ndia"]] if whm_on else 0.0

            use_food = False if values["food"] == "None" else True
            if use_food:
                for food in all_food:
                    if food["Name"] == values["food"]:
                        food_attack = food.get("Attack",0)
                        food_rangedattack = food.get("Ranged Attack",0)
                        food_accuracy = food.get("Accuracy",0)
                        food_rangedaccuracy = food.get("Ranged Accuracy",0)
                        food_magicaccuracy = food.get("Magic Accuracy",0)
                        food_magicattack = food.get("Magic Attack",0)
                        food_str = food.get("STR",0)
                        food_dex = food.get("DEX",0)
                        food_vit = food.get("VIT",0)
                        food_agi = food.get("AGI",0)
                        food_int = food.get("INT",0)
                        food_mnd = food.get("MND",0)
                        food_chr = food.get("CHR",0)
            else:
                food_attack,food_rangedattack,food_accuracy,food_rangedaccuracy,food_magicaccuracy,food_magicattack,food_str,food_dex,food_vit,food_agi,food_int,food_mnd,food_chr = [0 for k in range(13)]



            # Collect all of the buffs into a single dictionary which gets looped over in the main code to add towards your final stats.
            buffs = {"food": {"Attack": food_attack, "Ranged Attack": food_attack, "Accuracy": food_accuracy, "Ranged Accuracy":food_accuracy, "Magic Attack":food_magicattack, "Magic Accuracy":food_magicaccuracy, "STR":food_str,"DEX":food_dex, "VIT":food_vit, "AGI":food_agi, "INT":food_int, "MND":food_mnd, "CHR":food_chr,},
                     "brd": {"Attack": brd_attack, "Accuracy": brd_accuracy, "Ranged Accuracy": brd_rangedaccuracy, "Ranged Attack": brd_attack,"Haste":brd_haste},
                     "cor": {"Attack": cor_attack, "Ranged Attack": cor_attack, "Store TP": cor_stp, "Accuracy": cor_accuracy, "Magic Attack": cor_magicattack, "DA":cor_da, "Crit Rate": cor_critrate},
                     "geo": {"Attack": geo_attack, "Ranged Attack": geo_attack, "Accuracy": geo_accuracy, "Ranged Accuracy":geo_accuracy, "Magic Accuracy":geo_magicaccuracy, "Magic Attack":geo_magicattack, "STR":geo_str,"DEX":geo_dex, "VIT":geo_vit, "AGI":geo_agi, "INT":geo_int, "MND":geo_mnd, "CHR":geo_chr,"Haste":geo_haste},
                     "whm": {"Haste": whm_haste, "STR":whm_str,"DEX":whm_dex, "VIT":whm_vit, "AGI":whm_agi, "INT":whm_int, "MND":whm_mnd, "CHR":whm_chr}, # WHM buffs like boost-STR. Not tested
                     }

            # Define your enemy stats based on the enemy tab.
            enemy = {"Defense":int(values["enemy_defense"]),
                     "Evasion":int(values["enemy_evasion"]),
                     "Magic Defense":int(values["enemy_mdefense"]),
                     "Magic Evasion":int(values["enemy_mevasion"]),
                     "VIT":int(values["enemy_vit"]),
                     "INT":int(values["enemy_int"]),
                     "AGI":int(values["enemy_agi"]),
                    }

            # Decrease enemy stats based on debuffs selected.
            enemy["Defense"] *= (1-(dia_potency + frailty_potency)) if (1-(dia_potency + frailty_potency)) > 0.01 else 0.01
            enemy["Magic Defense"] = (enemy["Magic Defense"] - malaise_potency) if (enemy["Magic Defense"]- malaise_potency) > -50 else -50
            enemy["Evasion"] -= torpor_potency


            # We need to transfer the list of gear to check into a list of lists now. This will be used by the main code to check each piece, slot by slot.
            check_gear = [] # List of lists, containing dictionaries for items to be checked. This gets appended to later using the items in the GUI with checkboxes marked.
            check_slots = ["main","sub","ranged","ammo","head","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet"] # Slot names to check. This gets filtered later with .remove()
            remove_slots = []
            for s in check_slots:
                gear_to_check = []
                for val in values: # Format: value = <slot>: <itemname>
                    if type(val) == str:
                        # print(slot, val, val.split(":")[0],values[val])
                        if val.split(":")[0] == s and values[val]:
                            item_name = " ".join(val.split()[1:]).split(";;")[0]
                            gear_to_check.append(name2dictionary(item_name,all_gear))
                            # print(s,item_name) # Print gear to be checked
                if len(gear_to_check) > 0:
                    check_gear.append(gear_to_check)
                else:
                    remove_slots.append(s)
            for s in remove_slots:
                check_slots.remove(s)

            spell = values["select spell"]
            burst = values["magic burst toggle"]
            futae = values["futae toggle"]
            ebullience = values["ebullience toggle"]
            sneak_attack = values["sa toggle"]
            trick_attack = values["ta toggle"]
            footwork = values["footwork toggle"]
            impetus = values["impetus toggle"]

            
            kick_ws_footwork = True if "Kick" in ws_name and footwork else False # TODO: maybe use this later or delete it from here. we already define it in the other files anyway
            

            if event == "quicklook":
                from wsdist import weaponskill
                from set_stats import *
                gearset = set_gear(buffs, starting_gearset, main_job ,sub_job,impetus=impetus)
                quicklook_damage = weaponskill(main_job, sub_job, ws_name, enemy, gearset, np.average([min_tp, max_tp]), buffs, starting_gearset, False, False, spell, burst, futae, ebullience, sneak_attack, trick_attack, impetus, footwork)[0]
                window["quickaverage"].update(f"{'Average =':>10s} {int(quicklook_damage):>6d} damage")   

            elif event == "quicklook magic":
                from wsdist import weaponskill
                from set_stats import *
                gearset = set_gear(buffs, starting_gearset, main_job ,sub_job,impetus=impetus)
                quicklook_damage = weaponskill(main_job, sub_job, ws_name, enemy, gearset, np.average([min_tp, max_tp]), buffs, starting_gearset, False, True, spell, burst, futae, ebullience, sneak_attack, trick_attack, impetus, footwork)[0]
                window["quickaverage"].update(f"{'Average =':>10s} {int(quicklook_damage):>6d} damage")   

            elif event == "Run WS":
                from wsdist import run_weaponskill

                show_final_plot = values["show final plot"]
                best_set = run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset, show_final_plot, False, spell, burst, futae, ebullience, sneak_attack, trick_attack, impetus, footwork)
                window["copy best set"].update(disabled=False)
           
            elif event == "Run Magic":
                from wsdist import run_weaponskill

                show_final_plot = False
                best_set = run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset, show_final_plot, True, spell, burst, futae, ebullience, sneak_attack, trick_attack, impetus, footwork)
                window["copy best set"].update(disabled=False)

            # 
            elif event == "get stats":
                from set_stats import *
        
                # Defining the empty set lets us see the contribution to stats from gear vs base.
                # It also means it'll call the set_gear() class twice, so expect two print statements if testing/debugging with the "Calc sets" button.
                empty_set = {'main':Hitaki,'sub':Empty,'ranged':Empty,'ammo':Empty,'head':Empty,'body':Empty,'hands':Empty,'legs':Empty,'feet':Empty,'neck':Empty,'waist':Empty,'ear1':Empty,'ear2':Empty,'ring1':Empty,'ring2':Empty,'back':Empty,}
                empty_gearset = set_gear({"food":{},"brd":{},"cor":{},"geo":{},"whm":{}},empty_set, main_job, sub_job)

                gearset = set_gear(buffs, starting_gearset, main_job, sub_job, impetus=impetus) # put impetus here, otherwise it's effect won't show up
                dual_wield = gearset.gear['sub'].get('Type', 'None') == "Weapon"

                window["tab group"].Widget.select(2) # https://github.com/PySimpleGUI/PySimpleGUI/issues/415
                                
                base_stats = ["STR","DEX","VIT","AGI","INT","MND","CHR"]
                for k in base_stats:
                    player_value = f"{k}: {int(empty_gearset.playerstats[k]):3d}{'+' + str(int(gearset.playerstats[k])-int(empty_gearset.playerstats[k])):>5s}"
                    window[f"{k.lower()} stat"].update(f"{k}: {int(gearset.playerstats[k])}")
                    window[f"{k.lower()} stat"].set_tooltip(player_value)


                player_accuracy1 = int(gearset.playerstats['Accuracy1'])
                window["acc1 stat"].update(f"{'Accuracy1:':<16s} {player_accuracy1:>4d}")
                player_accuracy2 = int(gearset.playerstats['Accuracy2']) if dual_wield else 0
                window["acc2 stat"].update(f"{'Accuracy2:':<16s} {player_accuracy2:>4d}")
                player_attack1 = int(gearset.playerstats['Attack1'])
                window["atk1 stat"].update(f"{'Attack1:':<16s} {player_attack1:>4d}")
                player_attack2 = int(gearset.playerstats['Attack2']) if dual_wield else 0
                window["atk2 stat"].update(f"{'Attack2:':<16s} {player_attack2:>4d}")
                player_rangedaccuracy = int(gearset.playerstats['Ranged Accuracy'])
                window["racc stat"].update(f"{'Ranged Accuracy:':<16s} {player_rangedaccuracy:>4d}")
                player_rangedattack = int(gearset.playerstats['Ranged Attack'])
                window["ratk stat"].update(f"{'Ranged Attack:':<16s} {player_rangedattack:>4d}")

                player_magic_accuracy = int(gearset.playerstats['Magic Accuracy'])
                window["macc stat"].update(f"{'Magic Accuracy:':<20s} {player_magic_accuracy:>4d}")
                player_matk = int(gearset.playerstats['Magic Attack'])
                window["matk stat"].update(f"{'Magic Attack:':<20s} {player_matk:>4d}")
                player_magic_damage = int(gearset.playerstats['Magic Damage'])
                window["mdmg stat"].update(f"{'Magic Damage:':<20s} {player_magic_damage:>4d}")
                magic_burst_bonus = int(gearset.playerstats['Magic Burst Damage'])
                window["mbb stat"].update(f"{'Magic Burst Bonus:':<21s} {magic_burst_bonus:>3d}")
                magic_burst_bonus2 = int(gearset.playerstats['Magic Burst Damage II'])
                window["mbb2 stat"].update(f"{'Magic Burst Bonus II:':<21s} {magic_burst_bonus2:>3d}")

                wsd = int(gearset.playerstats['Weaponskill Damage'])
                window["wsd stat"].update(f"{'Weapon skill damage:':<21s} {wsd:>3d}")
                ws_bonus = int(gearset.playerstats['Weaponskill Bonus'])
                window["ws bonus stat"].update(f"{'Weapon skill trait:':<21s} {ws_bonus:>3d}")
                tp_bonus = int(gearset.playerstats['TP Bonus'])
                window["tp bonus stat"].update(f"{'TP Bonus:':<20s} {tp_bonus:>4d}")


                pdl = int(gearset.playerstats['PDL'])/100
                window["pdl gear stat"].update(f"{'PDL (gear):':<20s} {pdl:>4.2f}")
                pdl_trait = int(gearset.playerstats['PDL Trait'])/100
                window["pdl trait stat"].update(f"{'PDL (trait):':<20s} {pdl_trait:>4.2f}")

                qa = int(gearset.playerstats['QA'])
                window["qa stat"].update(f"{'Quad. Attack:':<21s} {qa:>3d}")
                ta = int(gearset.playerstats['TA'])
                window["ta stat"].update(f"{'Triple Attack:':<21s} {ta:>3d}")
                da = int(gearset.playerstats['DA'])
                window["da stat"].update(f"{'Double Attack:':<21s} {da:>3d}")
                crit_rate = int(gearset.playerstats['Crit Rate'])
                window["crit rate stat"].update(f"{'Crit. Rate:':<21s} {crit_rate:>3d}")
                crit_damage = int(gearset.playerstats['Crit Damage'])
                window["crit damage stat"].update(f"{'Crit. Damage:':<21s} {crit_damage:>3d}")

                stp = int(gearset.playerstats['Store TP'])
                window["stp stat"].update(f"{'Store TP:':<16s} {stp:>4d}")
                dw = int(gearset.playerstats['Dual Wield']) if dual_wield else 0
                window["dw stat"].update(f"{'Dual Wield:':<16s} {dw:>4d}")
                gear_haste = int(gearset.playerstats['Gear Haste'])
                window["gear haste stat"].update(f"{'Gear Haste:':<16s} {gear_haste:>4d}")
                magic_haste = gearset.playerstats['Magic Haste']*100
                window["magic haste stat"].update(f"{'Magic Haste:':<15s} {magic_haste:>5.1f}")
                ja_haste = int(gearset.playerstats['JA Haste'])
                window["ja haste stat"].update(f"{'JA Haste:':<16s} {ja_haste:>4d}")

                two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
                one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana","Hand-to-Hand"]
                magic = ["Elemental Magic", "Ninjutsu"]
                ranged_skills = ["Throwing", "Marksmanship", "Archery"]
                for k in sorted(one_handed+two_handed):
                    window[f"{k} skill display"].update(f"{k+':':<16s} {gearset.playerstats[f'{k} Skill']:>4d}")
                    window[f"{k} skill display"].set_tooltip(f"Total {k} skill from gear, excluding main/off-hand weapons.\nMain-hand: +{gearset.gear['main'].get(f'{k} Skill',0)}\nOff-hand: +{gearset.gear['sub'].get(f'{k} Skill',0)}")
                for k in sorted(ranged_skills+magic):
                    window[f"{k} skill display"].update(f"{k+':':<16s} {gearset.playerstats[f'{k} Skill']:>4d}")
 
                window["macc skill stat"].update(f"{'Magic Accuracy Skill:':<21s} {gearset.playerstats[f'Magic Accuracy Skill']-gearset.gear['sub'].get('Magic Accuracy Skill',0):>3d}")

                gear_haste = 25. if gear_haste > 25. else gear_haste
                ja_haste = 25. if ja_haste > 25. else ja_haste
                magic_haste = 448/1024*100. if magic_haste > 448/1024*100. else magic_haste
                total_haste = magic_haste + gear_haste + ja_haste

                delay = (1-total_haste/100)*(1-dw/100)
                delay_min = 0.2
                delay_reduction = 1-delay_min if delay < delay_min else 1-delay

                window["delay reduction stat"].update(f"{'Delay Reduction:':<16s} {delay_reduction*100:>4.1f}")

        # Copy the best set to the initial set tab for convenience:
        if event == "copy best set":
            window["tab group"].Widget.select(0) # https://github.com/PySimpleGUI/PySimpleGUI/issues/415
            for val in values:
                if type(val) == str:
                    if "start" == val[:5]:
                        window[val].update(False)
            for slot in best_set:
                # print(slot, best_set[slot]["Name2"],values[f"start{slot}: {best_set[slot]['Name2']}"])
                window[f"showstart {slot}"].update(image_data=item2image(best_set[slot]["Name"]))
                if f"start{slot}: {best_set[slot]['Name2']+';;'+main_job}" in window.AllKeysDict: # https://github.com/PySimpleGUI/PySimpleGUI/issues/1597
                    window[f"start{slot}: {best_set[slot]['Name2']+';;'+main_job}"].update(True)
                window[f"showstart {slot}"].set_tooltip(best_set[slot]["Name2"])

    except Exception as err:

        # Automatically move to the "Output" if something returns an error.
        # window["tab group"].Widget.select(2) # https://github.com/PySimpleGUI/PySimpleGUI/issues/415

        traceback.print_exc() # print the most recent error to the output tab.
                              # this is only the most recent. if you have a chain of errors, then you'll have to work your way up one at a time.


# window.set_min_size(window.size)
window.close()
