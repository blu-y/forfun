
import setup_path
import airsim
import WP_Parser
import os
import sys

# Desired Speed in m/s
desired_speed  = 5

# WayPoints Data Path
docs = os.path.join(sys.path[0], "WayPoints.txt")

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# TakeOff
print("Taking Off")
client.takeoffAsync().join()
print("Initializing")
way_points = []


# Create WayPoint Parser
WPP = WP_Parser.WP_Data(docs, None)

# If Found WayPoint Data
if WPP.IsFileOpen:
    print("GOGO")

    # LOOP
    con = 1
    while(1):

        # Ignore WaPoint #17
        if con == 17: con+=1
        # Get WayPoint Data index = con
        new = WPP.ReadData(con, "WP")

        # Proceed If Next WayPoint Exist
        if new:
            con += 1
            print(new.X, new.Y, new.Z)
            print(new.Xoff, new.Yoff, new.Zoff)
            print(int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1)
            print(float(new.X)/100, float(new.Y)/100, float(new.Z)/100, "\n")
            way_points.append([int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1])
            #client.moveToPositionAsync(int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1, 5).join()
            client.moveToPositionAsync(float(new.X)/100, float(new.Y)/100, float(new.Z)/100*-1, 5).join()
            client.rotateToYawAsync(int(new.ZR)).join()

        else:
            break

    # Return To First WayPoint
    new = WPP.ReadData(1, "WP")
    way_points.append([int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1])
    client.moveToPositionAsync(int(new.Xoff), int(new.Yoff), int(new.Zoff)*-1, 5).join()

else:
    print("Failed To open WayPoint File")
client.hoverAsync().join()
client.landAsync().join()


'''
client.moveByVelocityZAsync(-10, 0, -5, 3) 
                            x, vy, z, duration

'''