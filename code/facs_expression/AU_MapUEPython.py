# Import necessary modules for Unreal Engine operations, CSV file handling, and OS operations.

import unreal
import csv
import os

# Function to reset or initialize control rig parameters for a given frame to default or specified values.
def set(control_rig, curr_frame):
    # The commented-out lines below are examples of how to set positions and float values for various facial controls.
    # These lines are placeholders to illustrate the type of operations that can be performed within this function.
        
    # Set the position of left and right nose controls to a starting value for the current frame.
    #unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "CTRL_L_nose", curr_frame, start_value)
    #unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "CTRL_R_nose", curr_frame, start_value)
        
    # Reset the float values for brow down controls on both sides to 0.0 for the current frame.
    #unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_down", curr_frame, 0.0)
    #unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_down", curr_frame, 0.0)
        
    # The block below is commented out but includes examples of setting various facial controls.
    # This illustrates the extensive customization available for animating different parts of the face.

    '''
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "Ctrl_L_eye_blink", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "Ctrl_R_eye_blink", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_cheekRaiser", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_cheekRaiser", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "CTRL_R_mouth_pull", curr_frame, start_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "CTRL_L_mouth_pull", curr_frame, start_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "Ctrl_C_jaw", curr_frame, start_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseIn", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseIn", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "CTRL_L_mouth_depress_stretch", curr_frame, start_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "CTRL_R_mouth_depress_stretch", curr_frame, start_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "CTRL_L_nose", curr_frame, start_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_position(level_sequence, control_rig, "CTRL_R_nose", curr_frame, start_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseOut", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseOut", curr_frame, 0.0)
    '''
    # Examples of resetting specific Action Units (AUs) to a default state for the current frame.
    # This is crucial for animating facial expressions based on the Facial Action Coding System (FACS).
    # AU 1: Inner Brow Raiser
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseIn", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseIn", curr_frame, 0.0)
    # AU 2: Outer Brow Raiser
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseOut", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseOut", curr_frame, 0.0)
    # AU 4: Brow Lowerer
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_down", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_down", curr_frame, 0.0)
    # AU 5: Upper Eyelid Raiser
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_eyelidU", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_eyelidU", curr_frame, 0.0)
    # AU 6: Cheek Raiser
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_cheekRaise", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_cheekRaise", curr_frame, 0.0)
    # AU 7: Lower Eyelid Depressor
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_eyelidD", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_eyelidD", curr_frame, 0.0)
    # AU 9: Nose Wrinkler
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_nose_wrinkleUpper", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_nose_wrinkleUpper", curr_frame, 0.0)
    # Adjusting the nose position using a Vector2D to represent the X and Y axis adjustments.
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "CTRL_L_nose", curr_frame, [0.0,0.0])
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "CTRL_R_nose", curr_frame, [0.0,0.0])
    # AU 12: Lip Corner Puller
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_cornerPull", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_cornerPull", curr_frame, 0.0)
    # AU 15: Lip Corner Depressor
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_cornerDepress", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_cornerDepress", curr_frame, 0.0)
    # AU 16: Lower Lip Depressor
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_lowerLipDepress", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_lowerLipDepress", curr_frame, 0.0)
    # AU 20: Lip Stretcher
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_stretch", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_stretch", curr_frame, 0.0)
    # AU 23: Lip Tightener
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_tightenD", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_tightenD", curr_frame, 0.0)
    # AU 26: Jaw Drop
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "Ctrl_C_jaw", curr_frame, [0.0,0.0])

# Function to assign AU values to the control rig for animation. It takes AU values from a dictionary and applies them to the rig.
def assign(level_sequence, control_rig, curr_frame, au_values, currRowNum):
    
    # Retrieve AU values for the current row from the dictionary.
    au1_value = au_values["AU1"][currRowNum]
    au2_value = au_values["AU2"][currRowNum]
    au4_value = au_values["AU4"][currRowNum]
    au5_value = au_values["AU5"][currRowNum]
    au7_value = au_values["AU7"][currRowNum]
    au12_value = au_values["AU12"][currRowNum]
    au15_value = au_values["AU15"][currRowNum]
    au16_value = au_values["AU16"][currRowNum]
    au20_value = au_values["AU20"][currRowNum]
    au23_value = au_values["AU23"][currRowNum]
    au26_value = au_values["AU26"][currRowNum]
    # Transform values are prepared for certain AUs where applicable.
    transform_value = [au12_value, 0.0, 0.0]
    transform_value15 = [au15_value, 0.0, 0.0]
    transform_value16 = [au16_value, 0.0, 0.0]
    transform_value20 = [au20_value, 0.0, 0.0]
    transform_value23 = [au23_value, 0.0, 0.0]
    nose_value = [0.0, 0.0, 0.0]
    jaw_value = [0.0, 0.0, au26_value*2]
    # Apply the AU values to the control rig for the current frame, adjusting facial expressions accordingly.
    # Each call to the Unreal Engine API's `set_local_control_rig_float` or similar methods updates the rig.
    # The following blocks apply the AU values to the control rig, animating the MetaHuman's facial expressions.
    # Inner and outer brow raiser (AU 1 and AU 2)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseIn", curr_frame, au1_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseIn", curr_frame, au1_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseOut", curr_frame, au2_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseOut", curr_frame, au2_value)
    # Brow Lowerer (AU 4)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_down", curr_frame, au4_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_down", curr_frame, au4_value)
    # Upper Eyelid Raiser (AU 5), applying a negative value to invert the effect.
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_eyelidU", curr_frame, -1*au5_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_eyelidU", curr_frame, -1*au5_value)
    # Lower Eyelid Depressor (AU 7)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_eyelidD", curr_frame, au7_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_eyelidD", curr_frame, au7_value)
    # Nose Wrinkler (AU 9) and adjusting the nose position
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_nose_wrinkleUpper", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_nose_wrinkleUpper", curr_frame, 0.0)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "CTRL_L_nose", curr_frame, [0.0,0.0])
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "CTRL_R_nose", curr_frame, [0.0,0.0])
    # Lip Corner Puller (AU 12)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_cornerPull", curr_frame, au12_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_cornerPull", curr_frame, au12_value)
    # Lip Corner Depressor (AU 15)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_cornerDepress", curr_frame, au15_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_cornerDepress", curr_frame, au15_value)
    # Lower Lip Depressor (AU 16)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_lowerLipDepress", curr_frame, au16_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_lowerLipDepress", curr_frame, au16_value)
    # Lip Stretcher (AU 20)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_stretch", curr_frame, au20_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_stretch", curr_frame, au20_value)
    # Lip Tightener (AU 23)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_tightenD", curr_frame, au23_value)
    unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_tightenD", curr_frame, au23_value)
    # Jaw Drop (AU 26), using a Vector2D to represent the adjustment.
    unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "Ctrl_C_jaw", curr_frame, [0,au26_value])

# Function to read AU values from CSV files and populate a dictionary with these values.
def populateAUDictionary(ind):
    # Specify the paths to CSV files containing AU values for different emotions.
    links = ['/Users/zoelynch/Desktop/x_results1/goal_control/emotion_disappointed_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/goal_control/emotion_disappointed_1/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/goal_control/emotion_frustrated_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/goal_control/emotion_frustrated_1/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/goal_control/emotion_grateful_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/goal_control/emotion_grateful_1/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/goal_control/emotion_joyful_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/goal_control/emotion_joyful_1/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/safety_expected/emotion_devastated_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/safety_expected/emotion_devastated_1/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/safety_expected/emotion_relieved_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/safety_expected/emotion_relieved_1/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/safety_expected/emotion_resigned_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/safety_expected/emotion_resigned_1/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/safety_expected/emotion_surprised_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv',
             '/Users/zoelynch/Desktop/x_results1/safety_expected/emotion_surprised_1/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv'
             ]
    # Initialize a dictionary to hold AU values.
    au_values = {
        "AU1": [],
        "AU2": [],
        "AU4": [],
        "AU5": [],
        "AU7": [],
        "AU12": [],
        "AU15": [],
        "AU16": [],
        "AU20": [],
        "AU23": [],
        "AU26": []
    }
    
    # Open the specified CSV file and read AU values into the dictionary.
    with open(links[ind], newline='') as csvfile:

        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # Populate the AU value arrays with data from the CSV file, converting string values to floats.
            # Default to 0 if no value is provided for optional fields.
            au_values["AU1"].append(float(row[0]))
            au_values["AU2"].append(float(row[1]) if row[1] else 0)  # Default to 0 if no value
            au_values["AU4"].append(float(row[2]))
            au_values["AU5"].append(float(row[3]))
            au_values["AU7"].append(float(row[5]) if row[5] else 0)  # Default to 0 if no value
            au_values["AU12"].append(float(row[7]) if row[7] else 0)  # Default to 0 if no value
            au_values["AU15"].append(float(row[8]))
            au_values["AU16"].append(float(row[9]) if row[9] else 0)  # Default to 0 if no value
            au_values["AU20"].append(float(row[10]))
            au_values["AU23"].append(float(row[11]))
            au_values["AU26"].append(float(row[12]) if row[12] else 0)  # Default to 0 if no value
    return au_values

# Initialize a dictionary to store AU values for different facial expressions.
au_values = {
    "AU1": [],
    "AU2": [],
    "AU4": [],
    "AU5": [],
    "AU7": [],
    "AU12": [],
    "AU15": [],
    "AU16": [],
    "AU20": [],
    "AU23": [],
    "AU26": []
}

# Path to the CSV file containing AU values for a specific emotion (e.g., disappointment).
csv_file_path = '/Users/zoelynch/Desktop/x_results/goal_control/emotion_disappointed_0/gpt-4-0613_0shot_cot_0.0_10_0_parsed_answers_x.csv'

# Open and read the CSV file, populating the au_values dictionary with the data.
with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        # Convert string to float and handle missing values by setting them to 0.0.
        au_values["AU1"].append(float(row[0]))
        au_values["AU2"].append(float(row[1]) if row[1] else 0)  # Default to 0 if no value
        au_values["AU4"].append(float(row[2]))
        au_values["AU5"].append(float(row[3]))
        au_values["AU7"].append(float(row[5]) if row[5] else 0)  # Default to 0 if no value
        au_values["AU12"].append(float(row[7]) if row[7] else 0)  # Default to 0 if no value
        au_values["AU15"].append(float(row[8]))
        au_values["AU16"].append(float(row[9]) if row[9] else 0)  # Default to 0 if no value
        au_values["AU20"].append(float(row[10]))
        au_values["AU23"].append(float(row[11]))
        au_values["AU26"].append(float(row[12]) if row[12] else 0)  # Default to 0 if no value

# Load necessary Unreal Engine modules for Control Rig operations.
unreal.load_module('ControlRigDeveloper')
unreal.load_module('ControlRigEditor')

# Load the Control Rig Blueprint for a MetaHuman character.
rig_blueprint_path = '/Game/MetaHumans/Common/Face/Face_ControlBoard_CtrlRig.Face_ControlBoard_CtrlRig'

rig_blueprint = unreal.load_asset(rig_blueprint_path)
hierarchy = rig_blueprint.hierarchy

# Check if the rig blueprint was successfully loaded.
if not rig_blueprint:
    print("Control Rig Blueprint not found.")
    exit(1)

# Check if the level sequence asset was loaded successfully.
sequence_path = "/Game/AUMap"
level_sequence = unreal.load_asset(sequence_path, unreal.LevelSequence)

if not level_sequence:
    print("Level Sequence asset not found.")
    exit(1)
    
    
# Retrieve the control rigs within the level sequence.
rig_proxies = unreal.ControlRigSequencerLibrary.get_control_rigs(level_sequence)

# Select the first control rig proxy assuming it's the desired rig for animation.
rig_proxy = rig_proxies[1] # This may need adjustment based on the specific project setup.
print(rig_proxy)
control_rig = rig_proxy.control_rig

# Set up initial frame number and other variables for animation.

frameNum = 3
curr_frame = unreal.FrameNumber(frameNum)
control_value = 1.0 # Example control value for demonstration.

v = 0.0
start = [0.0, 0.0, 0.0]
start_value = [0.0, 0.0, 0.0]
transform_value = [1.0, 0.0, 0.0]
nose_value = [0.5, 0.0, 0.5]
jaw_value = [0.0, 0.0, 2.0]
k = 1
j = 0
# Demonstrate conditional animation logic based on the value of 'k'.

curr_frame = unreal.FrameNumber(frameNum)
while frameNum <= 10:
    curr_frame = unreal.FrameNumber(frameNum)
    set(control_rig, curr_frame)
    if frameNum == 4 : # begin from 4th frame so camera is post start up
        #happy
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_cheekRaise", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_cheekRaise", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_cornerPull", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_cornerPull", curr_frame, control_value)

    if frameNum == 5:
        #Sad
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseIn", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseIn", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_down", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_down", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_cornerDepress", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_cornerDepress", curr_frame, control_value)

    if frameNum == 6:
        #Surprise
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseIn", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseIn", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseOut", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseOut", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_eyelidU", curr_frame, -1*control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_eyelidU", curr_frame, -1*control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "Ctrl_C_jaw", curr_frame, [0,1.0])

    if frameNum == 7:
        #Fear
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseIn", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseIn", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_raiseOut", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_raiseOut", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_down", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_down", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_eyelidU", curr_frame, -1*control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_eyelidU", curr_frame, -1*control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_stretch", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_stretch", curr_frame, control_value)
        
    if frameNum == 8:
        #Disgust
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_nose_wrinkleUpper", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_nose_wrinkleUpper", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "CTRL_L_nose", curr_frame, [0.0,control_value])
        unreal.ControlRigSequencerLibrary.set_local_control_rig_vector2d(level_sequence, control_rig, "CTRL_R_nose", curr_frame, [0.0,control_value])
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_cornerDepress", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_cornerDepress", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_lowerLipDepress", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_lowerLipDepress", curr_frame, control_value)
    
    if frameNum == 9:
        #Anger
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_brow_down", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_brow_down", curr_frame, control_value)
        
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_eyelidU", curr_frame, -1*control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_eyelidU", curr_frame, -1*control_value)

        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_eye_eyelidD", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_eye_eyelidD", curr_frame, control_value)

        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_L_mouth_tightenD", curr_frame, control_value)
        unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_tightenD", curr_frame, control_value)
        
    if frameNum == 10:
            #contempt
            unreal.ControlRigSequencerLibrary.set_local_control_rig_float(level_sequence, control_rig, "CTRL_R_mouth_cornerPull", curr_frame, control_value)
    frameNum = frameNum + 1

numberCSVRows = 0
#Loop through the AI generated facial expression csv data
while numberRows < 16:
    au_values = populateAUDictionary(numberRows)
    while frameNum < 15 + numberRows*10+ 8 - 1:
        curr_frame = unreal.FrameNumber(frameNum)
        set(control_rig, curr_frame)
        if frameNum == 4 + numberRows*10 + 8:
            assign(level_sequence, control_rig, curr_frame,au_values,0)
        if frameNum == 5 + numberRows*10+ 8:
            assign(level_sequence, control_rig, curr_frame,au_values,1)
        if frameNum == 6 + numberRows*10+ 8:
            assign(level_sequence, control_rig, curr_frame,au_values,2)
        if frameNum == 7 + numberRows*10+ 8:
            assign(level_sequence, control_rig, curr_frame,au_values,3)
        if frameNum == 8 + numberRows*10+ 8:
            assign(level_sequence, control_rig, curr_frame,au_values,4)
        if frameNum == 9 + numberRows*10 + 8:
            assign(level_sequence, control_rig, curr_frame,au_values,5)
        if frameNum == 10 + numberRows*10+ 8 :
            assign(level_sequence, control_rig, curr_frame,au_values,6)
        if frameNum == 11 + numberRows*10+ 8 :
            assign(level_sequence, control_rig, curr_frame,au_values,7)
        if frameNum == 12 + numberRows*10+ 8 :
            assign(level_sequence, control_rig, curr_frame,au_values,8)
        if frameNum == 13 + numberRows*10+ 8 :
            assign(level_sequence, control_rig, curr_frame,au_values,9)
        frameNum = frameNum + 1
    numberRows = numberRows + 1

    print("Control rig AUs animation updated.")
    
