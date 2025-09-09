class AcmiLogger:
    def __init__(self, fname):
        self.log = open(fname, "w")
        self.log.write("FileType=text/acmi/tacview\nFileVersion=2.1\n")

    def __del__(self):
        self.log.close()

    def writeTime(self, time):
        self.log.write("#{:.2f}\n".format(time))

    def writeOnePlane(self, planeID, lon, lat, alt, roll, pitch, yaw, detailFlag=False):
        self.log.write(
            "{},T={}|{}|{:.3f}|{:.3f}|{:.3f}|{:.3f}".format(
                planeID, lon, lat, alt, roll, pitch, yaw
            )
        )
        if detailFlag:
            self.log.write(
                "Type=Air+FixedWing,Pilot=A618_{},Coalition=Allies,Color=Red,Country=ru,Name=F-18".format(
                    planeID
                )
            )
        self.log.write("\n")
