def test_Data(request):
    d=request.json
    gensql('insert','hotel_rooms',d)
    return("data_Inserted")
    
