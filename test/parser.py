import os
import threading
import time

#print(os.listdir())
t = threading.Thread()
lastBefehl = ""
lastArgs = []


class StripMethods:
    def colorWipe(self, color, wait_ms=50):
        ct = threading.currentThread()

        print("Doing shit")

        """Wipe color across display a pixel at a time."""
        for i in range(300):
                    if not getattr(ct, "change", False):
                            print("Setting Pixel #" + str(i))
                            time.sleep(wait_ms/1000.0)
                    else:
                            print("Applying change now...")
                            return

    def waiter(self, color, wait_ms=50):
        ct = threading.currentThread()
        while True:
            if getattr(ct, "change", False):
                print("Applying change now...")
                return

try:
    while True:
        #global t, lastBefehl, lastArgs

        f = open("./test/befehl.txt", "r")
        sub = f.readline().split("\n")
        #print(sub)
        change = int(sub[0])
        f.close()

        if change:
            print("Change detected!")

            t.change = True

            f = open("./test/befehl.txt", "r")
            lines = list(f)
            f.close()

            print(lines)
            lines[0] = "00\n"

            lastBefehl = lines[1].split("\n")[0]
            lastArgsSub = lines[2]

            print("Last Befehl: " + lastBefehl)
            print("Last Args: " + lastArgsSub)
            colors = lastArgsSub.replace('[', '').replace(']', '').split(",")
            colors = [ int(x) for x in colors ]
            print("Red: %s Green: %s Blue: %s" % (colors[0], colors[1], colors[2]))

            lastArgs.append(colors)
            print(tuple(*lastArgs))

            f = open("./test/befehl.txt", "w")
            f.writelines(lines)
            f.close()

            t = threading.Thread(target=getattr(StripMethods, lastBefehl), args=tuple(*lastArgs))
            t.start()

            #print(lines)
            #f.writelines(lines)
            
        



except KeyboardInterrupt:
    print("Terminating programm")

        