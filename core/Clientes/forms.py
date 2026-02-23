
from django import forms
import re


class LoginForm(forms.Form):
    usuario = forms.EmailField(label="Correo")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


class ContactForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=80,
        widget=forms.TextInput(attrs={
            "placeholder": "Tu nombre",
            "required": True,
        }),
    )

    email = forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={
            "placeholder": "tu@correo.com",
            "required": True,
        }),
    )

    asunto = forms.CharField(
        label="Asunto",
        max_length=120,
        widget=forms.TextInput(attrs={
            "placeholder": "¿Sobre qué te ayudamos?",
            "required": True,
        }),
    )

    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={
            "rows": 5,
            "placeholder": "Cuéntanos con detalle...",
            "required": True,
        }),
    )

    telefono = forms.CharField(
        label="Teléfono (opcional)",
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "+57 3xx xxx xxxx",
        }),
    )

    # Honeypot anti‑spam (campo oculto que los bots suelen llenar)
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned = super().clean()

        # Bloquear bots si llenan el honeypot
        if cleaned.get("website"):
            raise forms.ValidationError("Solicitud inválida.")

        # Validación opcional del teléfono (si lo envían)
        tel = cleaned.get("telefono")
        if tel:
            # Regla sencilla: mínimo 7 dígitos (ajústala a tu caso)
            solo_digitos = re.sub(r"\D+", "", tel)
            if len(solo_digitos) < 7:
                self.add_error("telefono", "Ingresa un teléfono válido (mínimo 7 dígitos).")

        return cleaned
