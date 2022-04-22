from compas_ui.rhino.forms import AttributesForm

attributes = {
    "a": 10,
    "b": True,
    "c": "hello",
    "d": (0, 0, 0),
}


form = AttributesForm(attributes.keys(), attributes.values())
form.show()

print(form.attributes)