from urllib.request import urlopen

def test_connection(module):
    production = False
    if (production == False):
        try:
            if(urlopen("http://localhost:5001/{}/test".format(module)).read() != b'OK'):
                print("Error: {} has issues!".format(module))
        except:
            print("Error: {} unreachable!".format(module))
    else:
        pass
    
test_connection("module001")
test_connection("module002")
test_connection("module003")
