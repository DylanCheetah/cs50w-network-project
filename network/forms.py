from django.forms import fields, Form, widgets


# Forms
# =====
class PostForm(Form):
    content = fields.CharField(max_length=1024, widget=widgets.Textarea({"cols": 150}))
