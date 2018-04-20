import socket
import connectfour
from collections import namedtuple

Connection = namedtuple('Connection', 'socket input output')


#
#
# SOCKET INTERACTION
#
#

def connect(host: str, port: int) -> Connection:
    '''Attempts to connect to a given host name and port.'''
    connect_socket = socket.socket()
    connect_socket.connect((host,port))

    connect_socket_input = connect_socket.makefile('r')
    connect_socket_output = connect_socket.makefile('w')

    return Connection(
        socket = connect_socket,
        input = connect_socket_input,
        output =  connect_socket_output)

def send_message(connection: Connection, message: str) -> None:
    '''Sends a given message to an established socket connection.'''
    connect_socket_output = connection.output

    connect_socket_output.write(message + '\r\n')
    connect_socket_output.flush()

def receive_response(connection: Connection) -> str:
    '''Receives a response from an established socket connection.'''
    connect_socket_input = connection.input

    return connect_socket_input.readline()[:-1]

def close(connection: Connection) -> bool:
    '''Terminates an established socket connection.'''

    connect_socket, connect_socket_input, connect_socket_output = connection

    connect_socket_input.close()
    connect_socket_output.close()
    connect_socket.close()
    print('Closing connection...')
    return False 

def interpret_response(connection: Connection,response: str) -> None:
    '''Decides how many responses to request/print based on a given
    response.'''

    list_of_responses = [response]
    
    if response=="OKAY":
        print_response(response)
        
        for i in range(2):
            response = receive_response(connection)
            list_of_responses.append(response)
            print_response(response)
        if "WINNER_YELLOW" in list_of_responses:
            print("Yellow wins.  The age of man has come to an end.")
            close(connection)
            
            
    elif response=="INVALID":
        print_response(response)
        print_response(receive_response(connection))
    elif response=="WINNER_RED":
        print("You win. Game over.")
        close(connection)
    else:
        print('socket responses do not match protocol.')
        close(connection)
        

def initial_protocol(connection: Connection, name: str) -> bool:
    send_message(connection,'I32CFSP_HELLO '+name)
    if receive_response(connection) == 'WELCOME '+name:
        send_message(connection,'AI_GAME')
        if receive_response(connection) != 'READY':
            print('socket responses do not match protocol.')
            close(connection)
            return False
    else:
        print('socket responses do not match protocol.')
        close(connection)
        return False
    return True
    
#
#
# USER INPUT
#
#

def input_host() -> str:
    '''Asks the user to specify a host until a valid response is given.'''
    while True:
        host = input('Host: ').strip()
        if len(host) == 0:
            print('Please specify a host to connect to (name or IP address)')
        else:
            return host

def input_port() -> int:
    '''Asks the user to specify a valid port to connect to.  The answer must be an integer
    between 0 and 65536'''
    while True:
        try:
            port = int(input('Port: ').strip())

            if port < 0 or port > 65535:
                print('Port must be an integer between 0 and 65535, please try again.')
            else:
                return port
        except ValueError:
            print('Port must be an integer between 0 and 65535, please try again.')

def input_username() -> str:
    '''Asks the user to specify a username to communicate with the server under.'''
    while True:
        name = input('Username: ').strip()
        if name.find(' ') != -1 or name.find('\t') != -1:
            print('Username must have no spaces, please try again.')
        else:
            return name

def print_response(response: str) -> None:
    '''Formats and prints response sent back from server.'''
    print('Response: ' + response)




#
#
#   ALMIGHTY USER INTERFACE
#
#

def user_interface() -> None:
    host = input_host()
    port = input_port()

    print('Connecting to {} (port {})...'.format(host,port))
    connection = connect(host,port)
    print('Wow, we have connected!')
    name = input_username()

    initial_protocol(connection,name)


    while True:
        user_message = input('Send: ')

        if user_message == '':
            break
        else:
            send_message(connection,user_message)
            response = receive_response(connection)
            interpret_response(connection,response) 
    

if __name__ == '__main__':
    user_interface()

