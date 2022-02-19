from django import forms

Quantity_Choice = [(i, str(i)) for i in range(1, 11)]
Size_Choice = (
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
)


class AddProductForm(forms.ModelForm):
    quantity = forms.TypedChoiceField(choices=Quantity_Choice,coerce=int)
    override = forms.BooleanField(required=False,initial=False, widget=forms.HiddenInput)