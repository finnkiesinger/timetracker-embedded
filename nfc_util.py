import subprocess


class NfcUtil():
    def nfc_raw(self):
        lines = subprocess.check_output(
            "/usr/bin/nfc-poll", stderr=open('/dev/null', 'w'))
        return lines

    def read_nfc(self):
        lines = self.nfc_raw()
        return lines
