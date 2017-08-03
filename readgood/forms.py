from django import forms


class AddBookForm(forms.Form):
    favorite = forms.BooleanField(required=False)
    rating = forms.ChoiceField(required=False, choices=(
        ('', '----'),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    ))
    book_list = forms.ChoiceField(required=False, choices=(
        ('', '----'),
        ('To Read', 'to-read'),
        ('Have Read', 'read'),
    ))
