import libkirara

api = libkirara.KiraraAPI()

api.loadAccount()
api.login()

other = 20
f5 = 0

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
		print('F-5 missions routine progress...' + str(i*20+j+1) + '/' + str(f5*5))
	api.fetchPresents()

print('Fucking Kirara for gems...Complete.')
input()