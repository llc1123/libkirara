import libkirara

api = libkirara.KiraraAPI()

for __ in range(300):
	
	api.getVersion()
	api.signUp()
	api.login()
	api.miscFirstLogin()
	api.gachaLoop()

	other = 20
	f5 = 5

	api.mission_refresh()
	api.mission_completeDaily()
	api.mission_completeWeekly()

	for i in range(other):
		api.mission_refresh()
		api.mission_completeOther()
		print('Other missions routine progress...' + str(i+1) + '/' + str(other))

	api.fetchPresents()

	for i in range(f5):
		for j in range(5):
			api.mission_completeF5()
			print('F-5 missions routine progress...' + str(i*5+j+1) + '/' + str(f5*5))
		api.fetchPresents()

	print('Fucking Kirara for gems...Complete.')

	api.gachaChrist()

	f = open('output.txt', 'a')
	f.write(api.uuid + ',' + api.accessToken + '\n')
	f.close()