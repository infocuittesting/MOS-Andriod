from sqlwrapper import *
def test_Data(request):
    d=  request.json
    gensql('insert','test_Table',d)
    return("data_Inserted")
    
