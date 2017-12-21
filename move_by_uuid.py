import libkirara

api = libkirara.KiraraAPI()

uuid, token = input('uuid,token: ').split(',')
api.manual(uuid, token)
api.login()
api.move()

input()