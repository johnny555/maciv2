import rclpy
from rclpy.node import Node
from rclpy.action.client import ActionClient
from control_msgs.action import FollowJointTrajectory
from control_msgs.msg import JointTolerance
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from builtin_interfaces.msg import Duration

def main():
    rclpy.init()
    node = Node("gripper_controller")
    logger = node.get_logger()
    move_to_position = -0.05

    ac = ActionClient(node, FollowJointTrajectory, "/gripper_controller/follow_joint_trajectory")
    ac.wait_for_server()

    logger.info("connected to server")
    traj = JointTrajectory()
    traj.joint_names = ["finger_joint"]
    traj.points = [JointTrajectoryPoint(positions=[move_to_position])]
    
    goal = FollowJointTrajectory.Goal()
    goal.trajectory = traj
    goal.goal_time_tolerance = Duration(sec=1)
    
    tol = [JointTolerance(name=n, position=0.001, velocity=0.001) for n in traj.joint_names]
    
    goal.path_tolerance = tol
    goal.goal_tolerance = tol
    
    res = ac.send_goal_async(goal)
    logger.info("waiting for goal complete")
    rclpy.spin_until_future_complete(node, res)
    

if __name__ == '__main__':
    main()
