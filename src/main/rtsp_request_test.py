'''
tests RtspRequest.py

there's probably a way to import modules in different dirs (i.e. put it into a test directory)
haven't figured that out yet in 2 mins or less.

this doesn't test depickling 
'''
import RtspRequest as rq

def main():
    
    testsRan = 0
    testsPassed = 0
    

    #bad seq num
    try:
        newReq = rq.RtspRequest('PAUSE', 0, 'myfile.txt')
        print("failed bad seq num")
        testsRan += 1
    except TypeError:
        testsRan += 1
        testsPassed += 1

    #bad req type
    try:
        newReq = rq.RtspRequest("Puase", 1, "myfile.txt")
        print('failed bad req type')
        testsRan += 1
    except ValueError:
        testsRan += 1
        testsPassed += 1

    #bad file type
    try:
        newReq = rq.RtspRequest("PAUSE", 1, 1)
        print("failed bad file type")
        testsRan += 1
    except TypeError:
        testsRan += 1
        testsPassed += 1

    #good obj
    try:
        newReq = rq.RtspRequest("PAUSE", 1, 'myfile.txt')
        testsPassed += 1
        testsRan += 1
    except TypeError:
        print("failed good constructor")
        testsRan += 1


    #update seq nm expect fail
    try:
        newReq.seqNum = 0
        testsRan += 1
    except ValueError:
        testsPassed +=1
        testsRan +=1

    # visual check of to-string
    print(newReq)

    #update seq num, pass
    try:
        newReq.seqNum = 2
        testsRan += 1
        testsPassed +=1
    except ValueError:
        testsRan +=1

    print(newReq)

    #update req type, pass
    try:
        newReq.reqType = "PLAY"
        testsRan += 1
        testsPassed +=1
    except ValueError:
        testsRan +=1


    #update req type, fail
    try:
        newReq.reqType = "booooogogo"
        testsRan += 1
    except ValueError:
        testsRan +=1
        testsPassed +=1

    #update filename , pass
    try:
        newReq.fileName = "newfile.txt"
        testsRan += 1
        testsPassed +=1
    except TypeError:
        testsRan +=1


    #update req type, fail
    try:
        newReq.reqType = "booooogogo"
        testsRan += 1
    except ValueError:
        testsRan +=1
        testsPassed +=1




    print("Tests ran:", testsRan, "Passed:", testsPassed/testsRan*100)


main()