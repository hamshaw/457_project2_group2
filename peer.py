import socket
import threading

'''
works for single
This is the Peer class.
each room within the building has a thermostat of the Peer class,
that holds all of its information and funtions.
the hardware would connect and control current temperature if implemented

made by Hannah Shaw, Brandon Mazurkiewicz, and Saif Fayed
'''


class Peer:
    def __init__(self, name, host, port):
        '''
        Each peer holds its own information, as well as the other rooms it connects to
        the main file controls the connection to other peers
        '''
        self.name = name
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.heat = False
        self.AC = False
        self.current = 70
        self.goal = 70
        self.stuck = False

    def set_goal(self, goal):
        '''
        if a peer is not "stuck" change the temperature to the new goal
        '''
        if not self.stuck:
            self.goal = int(goal)
            if self.current != self.goal:
                self.adjust()
        else:
            print("cannot override temperature")

    def stick(self, new: bool):
        '''
        sticks and unsticks a peer
        adds and removes the ability to set this room to a unique temperature
        '''
        self.stuck = new

    def set_current(self, current):
        '''
        would be controled by the hardware in a real life application
        if the new temperature is not what we set the room to, change the temperature
        '''
        self.current = int(current)
        if self.current != self.goal:
            self.adjust()

    def adjust(self):
        if self.goal > self.current:
            self.heat = True
            self.AC = False

        if self.goal < self.current:
            self.AC = True
            self.heat = False

        if self.goal == self.current:
            self.AC = False
            self.heat = False

    def connect(self, peer_host, peer_port):
        connection = socket.create_connection((peer_host, peer_port))

        self.connections.append(connection)
        print(f"Connected to {peer_host}:{peer_port}")

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address}")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_data(self, data):
        for connection in self.connections:
            try:
                connection.sendall(data.encode())
            except socket.error as e:
                print(f"Failed to send data. Error: {e}")
                self.connections.remove(connection)

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                ##print(f"Received data from {address}: {data.decode()}")
                data = data.decode()
                data = data.split()
                command = data[0]
                if command == 'unstick':
                    self.stick(False)
                else:
                    temp = int(data[1])
                    if command == 'stick':
                        self.stuck = False
                        self.set_goal(temp)
                        self.stick(True)
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def __str__(self):
        '''
        gives us each rooms state. prints to consol
        in real life application, this would be shown on the thermostat
        '''
        temp = f'Temperature: {self.current}'
        goal = f'Goal Temperature: {self.goal}'
        if self.heat:
            heat = 'on'
        else:
            heat = 'off'
        if self.AC:
            ac = 'on'
        else:
            ac = 'off'

        heatout = f'The heat is turned {heat}'
        acout = f'The AC is turned {ac}'
        return(f'{self.name} - \n{temp}\n{goal}\n{heatout}\n{acout}\n\n')
