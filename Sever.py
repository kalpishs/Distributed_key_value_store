from flask import Flask
app = Flask(__name__)
import os,sys
import  multiprocessing as mp

def info(title):
    print(title)
    print('module name:', __name__)
    if hasattr(os, 'getppid'):  # only available on Unix
        print('parent process:', os.getppid())
    print('process id:', os.getpid())


def startServer(inDebug, port):
    app.run(debug=inDebug, port=port)



if __name__ == '__main__':

    #info('Main Line Starting')

    procs = []
    for i in range(1,len(sys.argv)):
        port=int(sys.argv[i].split(':')[1])
        proc = mp.Process(target=startServer, args=(True,port))
        procs.append(proc)
        proc.daemon=True
        proc.start()

    for proc in procs:
        proc.join()
