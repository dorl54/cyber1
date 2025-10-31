"""
Author - Dor levek
Date   - 31/10/25
Server
"""


import socket
import datetime
import random
import logging


logging.basicConfig(level=logging.INFO,format='%(asctime)s - '
'%(levelname)s - %(message)s',filename='server.log',filemode='a')


server_name = "Dor's_Server"
IP = '0.0.0.0'
PORT = 8888
QUEUE_SIZE = 10


def handle_client(connection_socket, client_address):
    """
    The function manages the full conversation with a single connected
    client by continuously receiving commands.
    return: Nothing
    """


    logging.info(f'Client Connected from {client_address}')

    print('Client Connected')

    client_talking = True
    while client_talking:
        try:
            request = connection_socket.recv(4).decode()

            if not request:
                logging.info("Client Disconnected (empty request)")

                print("Client Disconnected (empty request)")
                break

            command = request.strip().upper()
            response = ""

            if (command == "TIME"):
                now = datetime.datetime.now()
                response = now.strftime("%H:%M:%S")

            elif (command == "NAME"):
                response = server_name

            elif (command == "RAND"):
                num = random.randint(1, 10)
                check_rand_value(num)
                response = str(num)

            elif (command == "EXIT"):
                logging.info("Client requested EXIT")

                print("Server Exiting")
                response = "bye"

                if response:
                    connection_socket.send(response.encode())

                client_talking = False
                continue

            else:
                response = f"I don't understand the command."
                logging.warning(f"Unknown command received: {command}")

            if response and command != "EXIT":
                connection_socket.send(response.encode())

        except ConnectionResetError:
            logging.warning("Client Disconnected (ConnectionResetError)")

            print("Server Disconnected (ConnectionResetError)")
            break
        except  Exception as e:
            logging.error(f"General error while handling client: {e}")

            print(f"General error: {e}")
            break

    logging.info('Closing client connection.')

    print('Closing client connection.')
    connection_socket.close()


def run_server():
    """
    The function sets up the server socket, binds it to a port,
    and then runs an infinite loop to wait for and accept new client connections.
    return Nothing
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        logging.info('Server Listening')

        print('Server Listening')

        while True:
            try:
                (connection_socket, client_address) = server_socket.accept()
                handle_client(connection_socket, client_address)

            except KeyboardInterrupt:
                logging.info("Server shutting down (KeyboardInterrupt)")
                break
            except Exception as e:
                logging.error(f'Error accepting connection: {e}')


                continue

    except OSError as e:
        logging.critical(f'FATAL ERROR starting server: {e}')


    finally:
        server_socket.close()
        logging.info('Server stopped.')

def check_rand_value(value):
    """
    It makes sure the random number is really between 1 and 10.
    return Nothing
    """

    assert 1 <= value <= 10, f"RAND value is bad! Got {value}, but it must be between 1 and 10."

    logging.debug(f"Assertion passed for RAND value: {value}")



if __name__ == "__main__":
    run_server()