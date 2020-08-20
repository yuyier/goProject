import socket
import csv

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('194.12.10.1', 4008))
serversocket.listen(5) # become a server socket, maximum 5 connections

dataElementsIndex={} #field:[size,usage,type,x]}

def csvToDict(filePath):
    dataElementsIndex.clear()
    with open(filePath) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONE) # change contents to floats
        for row in reader: # each row is a list
            dataElementsIndex[int(row[0])]=[row[1],int(row[2]),row[3]]
            
csvToDict("dataelements.csv")

def extractBitmaps(tcpPacketHex):
    bitmaps=[]
    packetLength=len(tcpPacketHex)
    chunkCount=int(packetLength/16)
    for i in range(0,chunkCount):
        start=i*16
        end=start+16
        bitmap=tcpPacketHex[start:end]
        tcpPacketBinary=eval("f'{"+hex(int(bitmap,16))+":0>42b}'")
        if(len(tcpPacketBinary)<64):
            tcpPacketBinary=(64-len(tcpPacketBinary))*'0'+tcpPacketBinary
        if(tcpPacketBinary[0]=='0'):
            bitmaps.append(tcpPacketBinary)
            return bitmaps
        else:
            bitmaps.append(tcpPacketBinary)
            
def parseBitmaps(bitmaps,dataElement):
    index=0
    for bitmap in bitmaps:
        count=1
        for dataElementState in list(bitmap):
            if dataElementState=='1':
                if dataElementsIndex[count][0]=="n..":
                    LLVAR=index+2
                    # print("["+str(count-1)+"] "+dataElementsIndex[count][2]+": "+dataElement[LLVAR:LLVAR+int(dataElement[index:LLVAR])])
                    index=LLVAR+int(dataElement[index:LLVAR])
                else:
                    # print("["+str(count-1)+"] "+dataElementsIndex[count][2]+": "+dataElement[index:index+dataElementsIndex[count][1]])
                    index=index+dataElementsIndex[count][1]
                    
            count=count+1

def response(mti):
    responseCode=mti[0:2]+"10"
    return responseCode.encode()
    

while True:
    connection, address = serversocket.accept()
    print(connection,address)
    buf = connection.recv(8000)
    print("len buf:"+str(len(buf)))
    if len(buf) > 0:
        #print(buf.hex()[4:]) #header
        iso8583Message=buf.hex()[14:] #tpdu
        print(iso8583Message)
        mti=iso8583Message[0:4]
        print("MTI: "+mti)
        bitmaps=extractBitmaps(iso8583Message[4:])
        print("Bitmap: "+str(bitmaps))
        # dataElement=iso8583Message[4+len(bitmaps)*16:]
        # parseBitmaps(bitmaps,dataElement)
        connection.send(response(mti).encode())
