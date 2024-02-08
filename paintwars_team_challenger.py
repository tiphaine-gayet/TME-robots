# Projet "robotique" IA&Jeux 2021
#
# Binome:
#  Prénom Nom: Tiphaine Gayet
#  Prénom Nom: Khadija Zamouri

import random

previous_distances = [0,0,0,0,0,0,0,0] #indice du sensor qui a capté une distance à 0
ss = ["sensor_front","sensor_front_right","sensor_right","sensor_back_right","sensor_back","sensor_back_left","sensor_left","sensor_front_left"]

def get_team_name():
    return "[ BALALAIKA ]" # à compléter (comme vous voulez)

def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]
    return sensors
    
def step(robotId, sensors):

    global previous_distances, ss
    sensors = get_extended_sensors(sensors)

	# aller tout droit par défaut
    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)


	#éviter notre team, suivre l'autre
    if sensors["sensor_front"]["isRobot"] :
        translation, rotation = hatebot(robotId, sensors)
        if not sensors["sensor_front"]["isSameTeam"]: # and robotId%2==0:
        	translation, rotation = followbot(robotId, sensors)
    
    elif sensors["sensor_front_right"]["isRobot"] :
    	translation, rotation = hatebot(robotId, sensors)
    	if not sensors["sensor_front_right"]["isSameTeam"]  : #and robotId%2==0:
        	translation, rotation = followbot(robotId, sensors)
    
    elif sensors["sensor_front_left"]["isRobot"] :
    	translation, rotation = hatebot(robotId, sensors)
    	if not sensors["sensor_front_left"]["isSameTeam"] : # and robotId%2==0:
        	translation, rotation = followbot(robotId, sensors)
    
    
    
    # éviter les murs
    if sensors["sensor_front_left"]["distance_to_wall"] < 1 or sensors["sensor_front"]["distance_to_wall"] < 1 or sensors["sensor_front_right"]["distance_to_wall"] < 1 :
    	translation, rotation = hatewall(robotId, sensors)
    	
    # si tout de même, le robot est bloqué depuis 2 tours (la distance du même sensor est à 0 depuis le tour dernier
    if previous_distances[int(robotId)]!= -1 and sensors[ss[previous_distances[int(robotId)]]]["distance"] <= 0.125:
    	rotation = random.uniform(-1,1)
    else :
    	previous_distances[int(robotId)] = -1
    	
	
    for i in range(8):
    	if sensors[ss[i]]["distance"] <=0.125:
    	    previous_distances[int(robotId)] = i
		

    return translation, rotation
    
    
def followbot(robotId, sensors):
    
    translation = 1 * sensors["sensor_front"]["distance_to_robot"]
    rotation = (1) * sensors["sensor_front_left"]["distance_to_robot"] + (-1) * sensors["sensor_front_right"]["distance_to_robot"]
    
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))


    return translation, rotation
    
def hatebot(robotId, sensors) :
    translation = 1 * sensors["sensor_front"]["distance_to_robot"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_robot"] + (1) * sensors["sensor_front_right"]["distance_to_robot"]
    
    if sensors["sensor_front"]["distance"] <=0.125 or sensors["sensor_front_right"]["distance"]<=0.125 or sensors["sensor_front_left"]["distance"]<=0.125:
    	translation, rotation =1,  random.uniform(-1,1)

    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation
    
def hatewall(robotId, sensors):
    translation = 1
    if sensors["sensor_front"]["distance"] < 1:
    	if random.random() < 0.75 : # va à gauche dans 75% des cas
    		rotation = -0.5
    	else :
    		rotation = +0.5
    if sensors["sensor_front_left"]["distance"] < 1 : # or sensors["sensor_front"]["distance"] < 1 :
        rotation = 0.5
    elif sensors["sensor_front_right"]["distance"] < 1:
        rotation = -0.5

    return translation, rotation
    
def followwall(robotId, sensors):
    
    translation = 1 * sensors["sensor_front"]["distance"]
    rotation = (0.5) * sensors["sensor_front_left"]["distance_to_wall"] + (-0.5) * sensors["sensor_front_right"]["distance_to_wall"]
    #if sensors["sensor_front_left"]["distance_to_wall"] <=0.125:
    #   rotation = 1
    
    # limite les valeurs de sortie entre -1 et +1
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))


    return translation, rotation
