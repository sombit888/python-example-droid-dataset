from dataclasses import dataclass
from franka_robotiq import PandaRobotiq # imports your robot and registers it
# imports the demo_robot example script and lets you test your new robot
#import mani_skill.examples.demo_robot as demo_robot_script
import custom_demo_robot as demo_robot_script
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


demo_robot_script.main()
