from compas_ui.app import App

a = App()
b = App()

assert a == b

a.session["test"] = 1

a.session.filepath = "temp/test1.json"
a.session["test"] = 1
a.session.record()
a.session.save()

a.session.filepath = "temp/test2.json"
a.session["test"] = 2
a.session.record()
a.session.save()

a.session.filepath = "temp/test3.json"
a.session.undo()
a.session.save()
