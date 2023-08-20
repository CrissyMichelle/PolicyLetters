from flask_wtf import FlaskForm
from wtforms import DateField, TimeField, StringField, SelectField, PasswordField, BooleanField, ValidationError
from wtforms.validators import InputRequired, Regexp, DataRequired
from wtforms.widgets import Input

class HTML5DateField(StringField):
    """Render wtf DateField into a string for html purposes"""
    widget = Input(input_type='date')
class HTML5DateTimeField(StringField):
    """Render wtf DateTimeField into a string for html purposes"""
    widget = Input(input_type='datetime-local')

class CustomFieldParam(StringField):
    def __init__(self, *args, sub_label=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.sub_label = sub_label

class ValidGeoLocation:
    """Validates input sent to Google Maps API"""
    def __init__(self, message=None):
        if not message:
            message = 'Please enter a valid address or LatLng.  (For example "Wahiawa, HI" or 21.497,-158.068).'
        self.message = message

    def __call__(self, form, field):
        pass

class GetDirectionsForm(FlaskForm):
    """Form for Google Maps API"""
    origin = StringField("Origin: ", validators=[InputRequired(), ValidGeoLocation()])
    destination = StringField("Destination: ", validators=[InputRequired(), ValidGeoLocation()])
    travelMode = SelectField("Select an option:", validators=[InputRequired()],
                             choices=[("DRIVING", "Driving"), ("WALKING", "Walking"), ("BICYCLING", "Biking"),
                                      ("TRANSIT", "Public Transit")])
