#!/usr/bin/env python3
import rospy
import moveit_commander
import sys
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class VisionPick:
    def __init__(self):
        rospy.init_node('vision_pick', anonymous=True)
        moveit_commander.roscpp_initialize(sys.argv)
        self.arm = moveit_commander.MoveGroupCommander("manipulator")
        self.arm.set_planning_time(15)
        self.arm.set_num_planning_attempts(10)
        self.arm.set_goal_tolerance(0.05)
        rospy.sleep(2)
        self.do_stand_and_pick()

    def send_joint_trajectory(self, positions, duration=3.0):
        jt = JointTrajectory()
        jt.header.stamp = rospy.Time.now()
        jt.joint_names = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
                          'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start = rospy.Duration(duration)
        jt.points.append(point)
        pub = rospy.Publisher('/eff_joint_traj_controller/command', JointTrajectory, queue_size=10)
        rospy.sleep(0.5)
        pub.publish(jt)
        rospy.loginfo("关节命令已发送：%s", positions)

    def do_stand_and_pick(self):
        rospy.loginfo("机械臂站立")
        self.send_joint_trajectory([0.0, -1.0, 2.0, -1.0, 0.0, 0.0], 3.0)
        rospy.sleep(5) 
      
        rospy.loginfo("规划到目标点 x=0.35 y=0.0 z=0.95")
        target_pose = PoseStamped()
        target_pose.header.frame_id = "base_link"
        target_pose.pose.position.x = 0.35
        target_pose.pose.position.y = 0.0
        target_pose.pose.position.z = 0.95
        target_pose.pose.orientation.w = 1.0

        self.arm.set_pose_target(target_pose)
        self.arm.set_start_state_to_current_state()  
        res = self.arm.plan()
        success = res[0]
        plan = res[1]
        if not success or not plan.joint_trajectory.points:
            rospy.logerr("规划失败")
            return

        rospy.loginfo("轨迹点数：%d，正在执行...", len(plan.joint_trajectory.points))
        jt = plan.joint_trajectory
        jt.header.stamp = rospy.Time.now()
        pub = rospy.Publisher('/eff_joint_traj_controller/command', JointTrajectory, queue_size=10)
        pub.publish(jt)
        rospy.loginfo("机械臂正在移向红色方块上方")
        rospy.sleep(5)

if __name__ == "__main__":
    vp = VisionPick()
    rospy.spin()
