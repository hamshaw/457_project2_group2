import peer

if __name__ == "__main__":
    ##list all rooms in the house
    room1 = peer.Peer('living room', "0.0.0.0", 8000)
    room1.start()

    room2 = peer.Peer('kitchen', "0.0.0.0", 8001)
    room2.start()

    room3 = peer.Peer('bedroom', "0.0.0.0", 8002)
    room3.start()

    ##make a list of all the rooms
    rooms = [room1, room2, room3]

    ##get the room that the process is running on and remove it from list of rooms
    ##set 'this' to current room
    thisroom = input()
    match thisroom:
        case '1':
            rooms.remove(room1)
            this = room1
        case '2':
            rooms.remove(room2)
            this = room2
        case '3':
            rooms.remove(room3)
            this = room3
        case _:
            raise("invalid room entry")

    ##establish a connection to each room
    for room in rooms:
        this.connect(room.host, room.port)

    while True:
        '''
        continuously accept new input
        these inputs would be from buttons on hardware of thermostat
        if implemented in a real building
        '''
        info = input()
        command = info.split()
        if command[0] == 'stick' or command[0] == 'unstick':
            ##if the command is stick or unstick
            ##then that needs to be sent to the other peers
            this.send_data(info)
            this.set_goal(command[1])
        else:
            ##other commands are just handled within this room
            ##only effects the current "peer"
            if command[0] == 'read':
                self.set_current(command[1])
            if command[0] == 'set':
                self.set_goal(command[1])
            if command[0] == 'status':
                print("In this room:")
                print(this)
                print()
                print("In the other rooms of the building: ")
                for room in rooms:
                    print(room)

