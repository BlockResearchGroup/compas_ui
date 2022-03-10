from compas_ui.session import Session

s = Session(name='test')

s['test'] = {}

s.record()

s['test']['a'] = 1

s.record()

s['test']['b'] = 2

s.record()

s.undo()
# s.undo()
# s.undo()

# s.record()

s.save()
