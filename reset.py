import libkirara

api = libkirara.KiraraAPI()

while True:

	api.getVersion()
	api.signUp()
	api.login()
	api.miscFirstLogin()
	api.gachaLoop()

	api.dropAll()
	
	api.mission_refresh()
	api.mission_completeDaily()
	api.mission_completeWeekly()

	for __ in range(250):
		api.mission_refresh()
		api.mission_completeOther()

	api.fetchPresents()

	api.move()

	f = open('output.txt', 'a')
	f.write(api.uuid + ',' + api.accessToken + ',' + api.moveCode + ',1234\n')
	f.close()
