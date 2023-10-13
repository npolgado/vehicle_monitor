
import rospy
from std_msgs.msg import Int64

def aquire_date():
   return 0xFFFFFFFFFFFF



if __name__ == "__main__":
   rospy.init_node('rideheight', anonymous=True)

   pub = rospy.Publisher("/rideheight", Int64, queue_size=100)
   rate = rospy.Rate(100)

   while not rospy.is_shutdown():
      data = aquire_date()
      pub.publish(data)
      rate.sleep()
