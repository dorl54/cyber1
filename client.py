"""
Author - Dor levek
Date   - 31/10/25
Server
"""

import socket
import logging

# New stuff for logging on the client
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s'
    ' - %(message)s',filename='client.log',filemode='a')

MAX_PACKET = 1024
IP = '127.0.0.1'
PORT = 8888

def run_client():
    """
    The run_client() function gets the program ready, sets up the connection.
    return nothing
    """

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info('Client socket created.')

    try:

        my_socket.connect((IP, PORT))
        logging.info(f'Successfully connected to {IP}:{PORT}')


        while True:
            request = input('Enter a command(TIME,NAME,RAND,EXIT): ')


            command_to_send = request.upper().ljust(4)[:4]

            logging.info(f"Sending command: {command_to_send.strip()}")
            my_socket.send(command_to_send.encode())

            if request.upper() == 'EXIT':
                break


            response = my_socket.recv(MAX_PACKET).decode()

            logging.info(f"Received response: {response}")
            print('Server responded: ' + response)


    except socket.error as err:
        logging.error('Received socket error ' + str(err))
        print('received socket error ' + str(err))
    except Exception as e:
        logging.critical(f'An unexpected error occurred: {e}')
        print(f'An unexpected error occurred: {e}')

    finally:
        logging.info('Connection closed.')
        my_socket.close()
        print('Connection closed.')



if __name__ == "__main__":
    run_client()