from compas_ui.session import Session

s = Session('test')

s['FoFin'] = {'mesh': None, 'a': 1}
s['FoFin']['b'] = 2

s.store()

s['Test'] = 1
s['FoFin']['c'] = 2

s.store()

s['Test'] = 2

s.store()

# s.restore()

print(s.data)
print(s.history)

s.save()

s.validate()
