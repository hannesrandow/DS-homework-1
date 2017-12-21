import threading
from socket import *
import struct
from time import sleep, time
from sudoku.common import protocol


class GameServerDiscovery(threading.Thread):
    def __init__(self, discovery_interval=2):
        print("Start Game Server Discovery.")
        server_address = ('0.0.0.0', protocol.multicast_group[1])
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.settimeout(2)
        self.sock.bind(server_address)      # bind to every address
        self.interval = discovery_interval  # call recv within this interval delays
        # Tell the operating system to add the socket to the multicast group
        # on all interfaces.
        group = inet_aton(protocol.multicast_group[0])
        mreq = struct.pack('4sL', group, INADDR_ANY)
        self.sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)
        self.found_game_servers = {}    # ipaddress: discovered_time
        self.lock = threading.Lock()    # mutual exclusion on found_game_servers
        self.start_timestamp = time()
        self._is_running = True         # as long as the user of the class requires it to run!
        self._thread_stopped = False    # signal for closing the socket
        threading.Thread.__init__(self) # initialize parent thread class
        self.start()    # start the thread

    def run(self):
        """ Discovery Loop (in a thread) """
        print("Game server discovery running..")
        while self._is_running:
            sleep(self.interval)
            try:
                msg, addr = self.sock.recvfrom(1024)
                if msg.decode("utf-8")  == protocol.service_name:
                    # print (msg, addr) # TODO: change to LOG.debug
                    self.lock.acquire()
                    self.found_game_servers[addr[0]] = time()
                    self.lock.release()
                else:
                    pass
                    # TODO: print following as a debug message
                    # print ("received a msg from %s but service_name does not match: %s" % (addr[0], msg.decode("utf-8") ))
            except timeout:
                continue
        self._thread_stopped = True

    def get_list(self, popup=None, progress_var=None):
        """ return servers that were alive at least in the past 10 seconds - might return empty list"""

        # give it a time to discover something
        tic = time()
        progress = 0
        progress_step = 100 / 5
        while (time()-tic) < 5:
            # print("too soon")
            if popup and progress_var: # this is only for the gui
                popup.update()
                progress += progress_step
                progress_var.set(progress)
            sleep(1)

        available_servers = []
        self.lock.acquire()
        for server_addr, timestamp in self.found_game_servers.items():
            if (time()-timestamp) < 10:
                available_servers.append(server_addr)
        self.lock.release()
        return available_servers

    def get_list_2(self):
        """ block to return at least a server that were alive at least in the past 10 seconds"""

        # wait until a server discovered
        while not self.found_game_servers:
            sleep(1)

        available_servers = []
        self.lock.acquire()
        for server_addr, timestamp in self.found_game_servers.items():
            if (time() - timestamp) < 10:
                available_servers.append(server_addr)
        self.lock.release()
        return available_servers

    def stop(self):
        """ stop the discovery thread and socket - do not forget to call after discovery job finished """
        self._is_running = False
        # busy waiting until thread is stopped
        while not self._thread_stopped:
            sleep(1)
        # now close the socket
        self.sock.close()


# usage sample (note that it requires protocol from the project)
if __name__ == "__main__":
    # mode 1
    print("mode 1..")
    game_server_discovery = GameServerDiscovery()
    print("discovered: ", game_server_discovery.get_list())
    game_server_discovery.stop()

    # mode 2
    print("mode 2..")
    game_server_discovery = GameServerDiscovery()
    print("discovered: ", game_server_discovery.get_list_2())
    game_server_discovery.stop()