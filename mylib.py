def list_attributes(o):
    for x in o.__dir__():
        try:
            print(str(x) + " " + str(getattr(o, x)))
        except:
            print(str(x) + " " + "err")
        print("-------x-------x-------x-------x-------x-------x-------x-------x-------x-------x-------x-------x-------x-------")