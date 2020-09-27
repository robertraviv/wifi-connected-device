from decouple import config
import nmap
from getmac import get_mac_address
from gtts import gTTS
from playsound import playsound


IP = config('WIFI_IP')
TRACK_DEVICE = config('GUEST_MAC')

# Create a notifiaction audio file
notification = gTTS('Tom has just connected to your network!')
notification.save('notify.mp3')


class Network(object):
    def __init__(self):
        self.ip = IP

    def networkscanner(self):
        network = self.ip + '/24'
        connected = False
        print('Scanning...')

        nm = nmap.PortScanner()
        while True:
            if connected:
                break
            nm.scan(hosts=network, arguments='-sn')
            hosts_lists = [(x, nm[x]['status']['state'])
                           for x in nm.all_hosts()]

            for host, status in hosts_lists:
                mac = get_mac_address(ip=host)
                print(f'Host: {host}\t MAC: {mac}')

                if mac == TRACK_DEVICE:
                    playsound('notify.mp3')
                    connected = True


if __name__ == "__main__":
    s = Network()
    s.networkscanner()
