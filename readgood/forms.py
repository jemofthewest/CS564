from django import forms


class AddBookForm(forms.Form):
    def clean(self):
        if 'read' in self.data:
            pass
        elif 'to-read' in self.data:
            pass
