from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField,  TextAreaField, DecimalField, validators, FormField, \
    IntegerField, PasswordField
from wtforms_components import SelectField, widgets
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_security import LoginForm, RegisterForm
from wtforms.fields.html5 import TelField


STATES = [
          ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
          ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'),
          ('HI', "Hawaii"), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IO', 'Iowa'), ('KS', 'Kansas'),
          ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
          ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'),
          ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'),
          ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
          ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
          ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
          ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
          ]
class ShareMyIdeaForm(FlaskForm):
    class Meta:
        # set to 1 week
        csrf_time_limit = 604800
        
    projname = StringField('Project Name ', validators=[validators.required(), validators.Length(3, 35)], render_kw={"maxlength": "35"})
    reqamount = DecimalField('Requested Grant Amount ', [validators.required(), validators.NumberRange(min=0, max=55000)], places=2)
    

    orgname = StringField('Organization Name ', validators=[validators.required(), validators.Length(3, 40)], render_kw={"maxlength": "40"})
    orgwebaddr = StringField('Organization Web Address ', validators=[validators.required(), validators.Length(3, 700)], render_kw={"maxlength": "700"})

    schoolname = StringField('School Name ', validators=[validators.Length(0, 35)], render_kw={"maxlength": "35"})
    schoolwebaddr = StringField('School Web Address ', validators=[validators.Length(0, 700)], render_kw={"maxlength": "700"})

    titles = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
    ]

    pititle = StringField('Title ', validators=[validators.required(), validators.Length(1, 3)], render_kw={"maxlength": "3"})
    pifirstname = StringField('First Name ', validators=[validators.required(), validators.Length(3, 14)], render_kw={"maxlength": "14"})
    pimi = StringField('Middle Initial ', validators=[ validators.optional(), validators.Length(0, 1)], render_kw={"maxlength": "1"})
    pilastname = StringField('Last Name ', validators=[validators.required(), validators.Length(3, 14)], render_kw={"maxlength": "14"})
    pisuffix = StringField('Name Suffix ', validators=[validators.optional(), validators.Length(0, 3)], render_kw={"maxlength": "3"})    
    picv = StringField('Curriculum Vitae web address ', validators=[validators.optional(), validators.Length(0, 700)], render_kw={"maxlength": "700"})    
    piemail = StringField('Email ', validators=[validators.required(), validators.Email()], render_kw={"maxlength": "700"})
    pitele = StringField('Telephone ', validators=[validators.required(), validators.Length(10, 10)], render_kw={"minlength": "10","maxlength": "10"})
    piaddr1 = StringField('Address 1 ', validators=[validators.required(), validators.Length(3, 30)], render_kw={"maxlength": "30"})
    piaddr2 = StringField('Address 2 ', validators=[validators.optional(), validators.Length(0, 30)], render_kw={"maxlength": "30"})
    picity = StringField('City ', validators=[validators.required(), validators.Length(3, 20)], render_kw={"maxlength": "20"})    
    pizip = StringField('Zip ', validators=[validators.required(), validators.Length(5, 5)], render_kw={"maxlength": "5", "minlength": "5"})

    othertitle = StringField('Title ', validators=[validators.Length(0, 3)], render_kw={"maxlength": "3"})
    otherfirstname = StringField('First Name ', validators=[validators.Length(0, 14)], render_kw={"maxlength": "14"})
    othermi = StringField('Middle Initial ', validators=[validators.Length(0, 1)], render_kw={"maxlength": "1"})
    otherlastname = StringField('Last Name ', validators=[validators.Length(0, 14)], render_kw={"maxlength": "14"})
    othersuffix = StringField('Name Suffix ', validators=[validators.Length(0, 3)], render_kw={"maxlength": "3"})
    otheremail = StringField('Email ', validators=[validators.optional(),validators.Email()], render_kw={"maxlength": "700"})
    othertele = StringField('Telephone ', validators=[validators.optional(), validators.Length(10, 10)], render_kw={"minlength": "10","maxlength": "10"})
    otheraddr1 = StringField('Address 1 ', validators=[validators.Length(0, 30)], render_kw={"maxlength": "30"})
    otheraddr2 = StringField('Address 2 ', validators=[validators.Length(0, 30)], render_kw={"maxlength": "30"})
    othercity = StringField('City ', validators=[validators.Length(0, 20)], render_kw={"maxlength": "20"})
    #otherstate = SelectField('State', validators=[validators.optional()], validate_choice=False)
    otherzip = StringField('Zip ', validators=[validators.optional(), validators.Length(5, 5)], render_kw={"maxlength": "5", "minlength": "5"})

    goal = TextAreaField('Research Goal ', validators=[validators.required(), validators.Length(3, 360)], render_kw={"rows": 3,"maxlength": "360"})
    description = TextAreaField('Project Description ', validators=[validators.required(), validators.Length(3, 2400)], render_kw={"rows": 3,"maxlength": "2400"})
    aboutpeople = TextAreaField('About the PI and other team members ', validators=[validators.Length(0, 1500)], render_kw={"rows": 3,"maxlength": "1500"})
    relevance = TextAreaField('Relevance of the project ', validators=[validators.required(), validators.Length(3, 2400)], render_kw={"rows": 3,"maxlength": "2400"})
    dissemination = TextAreaField('Dissemination ', validators=[validators.required(), validators.Length(3, 900)], render_kw={"rows": 3,"maxlength": "900"})
    projother = TextAreaField('Other Information ', validators=[validators.Length(0, 900)], render_kw={"rows": 3,"maxlength": "900"})

    submit = SubmitField('Submit')

    def validate(self, extra_validators=None):
        if super().validate(extra_validators):

            # your logic here e.g.
            if not (self.picv.data or self.aboutpeople.data):
                self.picv.errors.append('Either the PI’s CV web address or the About the PI… field must have a value.')
                return False
            else:
                return True

        return False


class sendDocumentForm(FlaskForm):
    irsfield = FileField(validators=[FileRequired(), FileAllowed(['pdf', 'jpg', 'png'])])
    budfield = FileField(validators=[FileRequired(), FileAllowed(['xls', 'xlsx'])])


class LoginOverrideForm(LoginForm):
    """Overriding the flask security login form so that we can use emails instead of
    usernames"""
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()],
                        render_kw={"maxlength": "70"})
    submit = SubmitField(label="SIGN IN")


class RegisterOverrideForm(RegisterForm):
    class Meta:
        csrf_time_limit = 604800

    # title = SelectField('Title', choices=[(1, 'Mr'), (2, 'Mrs'), (3, 'Miss'),(4, 'Ms'),(5, 'Dr')],
    #                     validators=[validators.DataRequired()], coerce=int)
    first_name = StringField('First Name ', validators=[validators.DataRequired(), validators.Length(min=3, max=30)],
                             render_kw={"maxlength": "50"})
    # middle_initial = StringField('MI', validators=[validators.DataRequired(), validators.Length(max=1)],
    #                              render_kw={"maxlength": "1"})
    last_name = StringField('Last Name ', validators=[validators.DataRequired(), validators.Length(min=3, max=30)],
                            render_kw={"maxlength": "50"})
    password = PasswordField('Password ', validators=[validators.DataRequired(), validators.Length(8, 50)],
                             render_kw={"minlength": "8"})
    password_confirm = PasswordField('Confirm Password ', validators=[validators.DataRequired(), validators.Length(8, 50)],
                                     render_kw={"minlength": "8"})
    # suffix = StringField('Suffix', validators=[validators.optional(), validators.Length(0, 3)],
    #                      render_kw={"maxlength": "3"})
    # Uncomment this field and the field in the template to enable captcha
    recaptcha = RecaptchaField()
    submit = SubmitField(label="CREATE NEW ACCOUNT")


class MessageForm(FlaskForm):
    class Meta:
        csrf_time_limit = 604800

    subject = SelectField('Select a subject', coerce=int)
    name = StringField('Name ', validators=[validators.DataRequired(), validators.Length(3, 50)],
                       render_kw={"maxlength": "50"})
    email = StringField('Email ', validators=[validators.DataRequired(), validators.Email()],
                        render_kw={"maxlength": "70"})

    message = TextAreaField('Message ', validators=[validators.Length(1, 480)],
                            render_kw={"rows": 3, "maxlength": "500"})

    submit = SubmitField('Submit')


class CompleteRegistrationForm(FlaskForm):
    class Meta:
        csrf_time_limit = 604800

    org = StringField('Organization Name', validators=[validators.DataRequired(), validators.Length(3, 40)],
                       render_kw={"maxlength": "40"})
    school = StringField('School Name', validators=[validators.optional(), validators.Length(3, 35)],
                       render_kw={"maxlength": "35"})
    position = StringField('Position ', validators=[validators.DataRequired(), validators.Length(3, 35)],
                       render_kw={"maxlength": "35"})
    tele = StringField('telephone', validators=[validators.DataRequired()])
    adder1 = StringField("Address", validators=[validators.DataRequired()], render_kw={"maxlength": "30"})
    adder2 = StringField("Address 2", validators=[validators.optional()], render_kw={"maxlength": "30"})
    city = StringField("City", validators=[validators.DataRequired()], render_kw={"maxlength": "20"})
    zipcode = StringField("Zipcode", validators=[validators.DataRequired()], render_kw={"maxlength": "5"})
    state = SelectField("State", choices=STATES, validators=[validators.DataRequired()])
    submit = SubmitField('Submit')
