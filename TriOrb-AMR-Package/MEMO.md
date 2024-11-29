
ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 0,\
    "'"task"'" : \
    [\
        "'"task01"'"\
    ]\
}'}"

ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 0,\
    "'"task"'" : \
    [\
        "'"task02"'"\
    ]\
}'}"

ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 0,\
    "'"task"'" : \
    [\
        "'"task03"'"\
    ]\
}'}"


ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 0,\
    "'"task"'" : \
    [\
        "'"task05"'",\
        "'"task06"'"\
    ]\
}'}"



ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 0,\
    "'"task"'" : \
    [\
        "'"task01"'",\
        "'"task02"'",\
        "'"task03"'",\
        "'"task05"'"\
    ]\
}'}"


ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 99,\
    "'"task"'" : \
    [\
        "'"task02"'",\
        "'"task03"'",\
        "'"task05"'",\
        "'"task01"'"\
    ]\
}'}"


ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 0,\
    "'"task"'" : \
    [\
        "'"task02"'",\
        "'"task03"'",\
        "'"task05"'"\
    ]\
}'}"


ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 10,\
    "'"task"'" : \
    [\
        "'"task01"'",\
        "'"task05"'"\
    ]\
}'}"

ros2 topic pub -1 /fleet/schedule/new std_msgs/msg/String \
"{data : '{\
    "'"loop"'" : 10,\
    "'"task"'" : \
    [\
        "'"task05"'",\
        "'"task01"'"\
    ]\
}'}"
