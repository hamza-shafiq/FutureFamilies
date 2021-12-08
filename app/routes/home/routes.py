import os
import time
from datetime import date, datetime
from typing import List
import re
from flask_mail import Message
from flask import redirect, request, jsonify, url_for, render_template, flash, Markup
from werkzeug.utils import secure_filename
import secrets
from flask_security import logout_user, login_required, current_user
from app.extensions import db, mysql, mail
from . import bp
from itertools import zip_longest

from flask_login import current_user
from flask_security.utils import hash_password
from flask_security.changeable import change_user_password

from app.forms import sendDocumentForm, ShareMyIdeaForm, MessageForm, CompleteRegistrationForm, RegisterOverrideForm

from flask_security.registerable import register_user


conn = mysql.connect()
crsr = conn.cursor()
codes = {"Researcher news": "news",
         "Grant request comment": "grantc",
         "Grant request question": "grantq",
         "APKAS curriculum": "apkas",
         "Something else": "other",
         "Pilot testing": "pilot",
         "Submitting research for publication": "report",
         "Research topics": "restopic",
         "Website content": "webcont",
         "Website issue": "webtech"
         }

@bp.route("/login-redirect/")
@login_required
def login_redirect():
    if current_user.reg_complete:
        return redirect(url_for('home.home'))
    else:  # Add other redirects based on role here.
        return redirect(url_for('home.registration_continued'))

@bp.route("/registration_continued", methods=["GET", "POST"])
def registration_continued():
    if current_user.reg_complete:
        return redirect(url_for('home.home'))
    form = CompleteRegistrationForm()
    if form.password.data != form.confirm_password.data:
        return render_template("/registration_continued.html", form=form, error="Password Mismatch")

    if request.method == 'POST' and form.validate():
        # change_user_pas/sword(current_user._get_current_object(), form.password.data)
        # statement1 = f"""INSERT into userfirst (emailaddress) VALUES('{current_user.email}')"""
        # statement2 = f"""
        # INSERT INTO usercpt (emailaddress, orgname, schoolname, position, tele, addr1, addr2, city, state, zip)
        # VALUES ('{current_user.email}', '{form.org.data}', '{form.school.data}', '{form.position.data}',
        #         {form.tele.data}, '{form.adder1.data}', '{form.adder2.data}', '{form.city.data}',
        #         '{form.state.data}', '{form.zipcode.data}')
        #              """
        statement3 = f"""UPDATE user SET reg_complete = 1, password = '{hash_password(form.password.data)}' WHERE emailaddress = '{current_user.email}'"""
        # crsr.execute(statement1)
        # crsr.execute(statement2)
        crsr.execute(statement3)
        conn.commit()
        return redirect(url_for('home.home'))
    else:
        print(form.errors)
    return render_template("/registration_continued.html", form=form)


@bp.route("/custom-register/", methods=["POST"])
def custom_register():
    form = RegisterOverrideForm(request.form)
    form.password.data = "12341234"
    form.password_confirm.data = "12341234"
    if request.method == 'POST' and form.validate_on_submit():
        register_user(form)

    return render_template('/security/login_user.html', register_user_form=form)


@bp.route("/")
def home():
    return render_template("/home.html")


@bp.route("/why/")
def why():
    return render_template("why.html")


@bp.route("/scienceaccumulating/")
def scienceaccumulating():
    return render_template("scienceaccumulating.html")


@bp.route("/earlyyears/")
def earlyyears():
    return render_template("earlyyears.html")


@bp.route("/parenting/")
def parenting():
    return render_template("parenting.html")


@bp.route("/thechallenge/")
def thechallenge():
    return render_template("thechallenge.html")


@bp.route("/opportunity/")
def opportunity():
    return render_template("opportunity.html")


@bp.route("/ourwork/")
def ourwork():
    return render_template("ourwork.html")


@bp.route("/history/")
def history():
    return render_template("history.html")


@bp.route("/activities/")
def activities():
    return render_template("activities.html")


def send_mail(subject: str, recipients: List[str], body: str, bcc: List[str]):
    msg = Message(sender=('system@strongfam.org', bcc[0]), subject=subject, recipients=recipients, body=body, bcc=bcc)
    mail.send(msg)


def send_thank_you(subj: str, recipients: List[str], bcc: List[str]):
    body = 'Thank you for your message. We will get back with you soon.'
    subject = 'Thank you for your message'
    msg = Message(sender=(bcc[0], bcc[0]), subject=subject, recipients=recipients, body=body, bcc=bcc)
    mail.send(msg)


@bp.route("/submit_thank_you/", methods=["GET", "POST"])
def submit_thank_you(origin=None):
    return render_template("submit_thank_you.html", origin=origin)


@bp.route("/joinin/", methods=["GET", "POST"])
def joinin():
    form = MessageForm(request.form)
    query = """
    SELECT subjectdesc, menusequence
    FROM messagesubj
    WHERE menusequence is not null and active = True
    ORDER BY menusequence
    """

    crsr.execute(query)
    dropdown = [(sequence, subject) for subject, sequence in crsr]
    form.subject.choices = dropdown
    if request.method == 'POST' and form.validate():
        msgdate = datetime.now().timestamp()
        subject_code = [sbj for idx, sbj in dropdown if idx == form.subject.data][0]
        visname = form.name.data
        visemailaddr = form.email.data
        message = form.message.data
        code = codes[subject_code]
        current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        statement = f"INSERT INTO message (msgdate, subjectcode, visname, visemailaddr, message) " \
                    f"VALUES('{current}', '{code}', '{visname}', '{visemailaddr}', '{message}');"
        print(statement)
        crsr.execute(statement)
        select1 = f"SELECT msgnr from message where msgdate = '{current}'"
        crsr.execute(select1)
        msgnr = crsr.fetchone()
        select = f"SELECT sffsendemailaddr, destemailaddr from outmsgque where msgnr = {msgnr[0]};"
        crsr.execute(select)
        destinations = crsr.fetchall()
        thankyou_sent = False
        for destination in destinations:
            sffemail, visemail = destination

            body = f"""
            SFF received the following message:\n
            1. Date: {datetime.today().strftime("%m/%d/%Y %I:%M %p")}
            2. Email Subject {subject_code}
            3. From: {form.name.data}
            4. Sender Email: {form.email.data}\n
            5. Message: \n{form.message.data}
            """
            send_mail(subject=f'Automated SFF Message {subject_code}',
                      recipients=[sffemail, ],
                      body=body,
                      bcc=[sffemail, ]
                      )
            if thankyou_sent is False:
                send_thank_you(subj=subject_code, recipients=[visemail], bcc=[sffemail, ])
                thankyou_sent = True


        # statement = f"UPDATE outmsgque SET msgsent_YN = 1, minsendtime = {datetime.now().timestamp()} WHERE msgdate = {msgdate});"
       # crsr.execute(statement)

    return render_template("joinin.html", form=form)


@bp.route("/results/")
def results():
    return render_template("results.html")


@bp.route("/phase1/")
def phase1():
    return render_template("phase1.html")


@bp.route("/statestandards/")
def statestandards():
    return render_template("statestandards.html")


@bp.route("/questionnaire/")
def questionnaire():
    return render_template("questionnaire.html")


@bp.route("/curriculum/")
def curriculum():
    return render_template("curriculum.html")


@bp.route("/whatlearned/")
def whatlearned():
    return render_template("whatlearned.html")


@bp.route("/grants/")
def grants():
    return render_template("grants.html")


@bp.route("/whyapply/")
def whyapply():
    return render_template("whyapply.html")


@bp.route("/focus/")
def focus():
    return render_template("focus.html")


@bp.route("/details/")
def details():
    return render_template("details.html")


@bp.route("/shareidea/")
def shareidea():
    return render_template("shareidea.html")


@bp.route("/whatexpect/")
def whatexpect():
    return render_template("whatexpect.html")


@bp.route("/forfuture/")
def forfuture():
    return render_template("forfuture.html")


@bp.route("/about/")
def about():
    return render_template("about.html")


@bp.route("/goal/")
def goal():
    return render_template("goal.html")


@bp.route("/thankyou/")
def thankyou():
    return render_template("thankyou.html")


@bp.route("/board/")
def board():
    return render_template("board.html")


@bp.route("/references/")
def references():
    return render_template("references.html")


@bp.route("/contactus/", methods=["GET", "POST"])
def contactus():
    form = MessageForm(request.form)
    query = """
        SELECT subjectdesc, menusequence
        FROM messagesubj
        WHERE menusequence is not null and active = True
        ORDER BY menusequence
        """

    crsr.execute(query)
    dropdown = [(sequence, subject) for subject, sequence in crsr]
    form.subject.choices = dropdown
    if request.method == 'POST' and form.validate():
        subject = [sbj for idx, sbj in dropdown if idx == form.subject.data][0]
        body = f"""
            SFF received the following message:\n
            1. Date: {datetime.today().strftime("%m/%d/%Y %I:%M %p")}
            2. Email Subject {subject}
            3. From: {form.name.data}
            4. Sender Email: {form.email.data}\n
            5. Message: \n{form.message.data}
            """
        send_mail(subject=f'Automated SFF Message {subject}',
                  sender='testdummysff@gmail.com',
                  recipients=[form.email.data],
                  body=body
                  )

    return render_template("contactus.html",form=form)


@bp.route("/terms/")
def terms():
    return render_template("terms.html")


@bp.route("/login/")
def login():
    return render_template("/layouts/login.html")

@bp.route('/logout/', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('logout'))


# @bp.route("/whyintro_cont/")
# def whyintro_cont():
#    return render_template("/content/whyintro_cont.html",\
#    itemtxt1 = itemtxt[0], itemtxt2 = itemtxt[1],\
#    itemtxt3 = itemtxt[2], itemtxt4 = itemtxt[3],\
#    itemtxt5 = itemtxt[4], itemtxt6 = itemtxt[5],\
#    itemtxt7 = itemtxt[6], itemtxt8 = itemtxt[7])

# @bp.route("/foot/")
# def foot():
#    return render_template("/foot.html",\
#    projaddr1 = projaddr1,\
#    projaddr2 = projaddr2,\
#    projname = projname,\
#    copyrightmsg = copyrightmsg)

#  and newprojnum is null (in the cursor select below).
@bp.route('/ajax/find-project', methods=['GET'])
def findproject():
    reqtype = request.args['reqtype']
    projectnumber = request.args['projectnumber']
    submissiondate = request.args['submissiondate']
    pilastname = request.args['pilastname']

    crsr.execute(
        "SELECT count(*) FROM idea1 WHERE projnum = %s and DATE_FORMAT(subdate,'%%Y-%%m-%%d') = %s and pilastname=%s and newprojnum is null",
        (projectnumber, submissiondate, pilastname))
    # fetch all rows and store as a set of tuples
    (number_of_rows,) = crsr.fetchone()

    status = "error"
    msg = "No Project found. Please try with different details"
    url = ""
    code = secrets.token_urlsafe(16)

    if (number_of_rows > 0):
        status = "success"
        msg = "Project found!. Please wait, redirecting..."
        if reqtype == 'document':
            url = url_for('senddocument', secret=code, pnum=projectnumber, reqtype=reqtype)
        else:
            url = url_for('sharemyidea', secret=code, pnum=projectnumber, reqtype=reqtype)

    return jsonify(status=status, url=url, message=msg)


@bp.route('/revise-my-ideas', methods=['GET'])
@login_required
def reviseideas():
    if not current_user.reg_complete:
        return redirect(url_for('home.registration_continued'))
    crsr.execute(f"select ideanum from userideafinal where emailaddress = '{current_user.email}'")
    finalproj = [x[0] for x in crsr.fetchall()]
    crsr.execute(f"select ideanum from useridea where emailaddress = '{current_user.email}'")
    projs = [x[0] for x in crsr.fetchall()]
    table_data = list(zip_longest(projs, finalproj))
    return render_template('reviseidea.html', data=table_data)


@bp.route('/share-my-idea', methods=['GET'])
@login_required
def sharemyidea():
    if not current_user.reg_complete:
        return redirect(url_for('home.registration_continued'))
    existingprojnum = ''
    if 'pnum' in request.args:
        existingprojnum = request.args['pnum']

    form = ShareMyIdeaForm(request.form)
    crsr.execute('SELECT code,name FROM states')
    # fetch all rows and store as a set of tuples
    statelist = crsr.fetchall()
    return render_template('sharemyidea.html',
                           form=form, statelist=statelist, existingprojnum=existingprojnum)



@bp.route('/ajax/save-my-idea', methods=['POST'])
def savemyidea():
    form = ShareMyIdeaForm(request.form)
    status = 'error'
    if form.validate_on_submit():
        existingprojnum = request.form['existingprojnum'] if request.form['existingprojnum'] != '' else None
        projname = form.projname.data
        reqamount = float(form.reqamount.data)
        orgname = form.orgname.data
        orgwebaddr = form.orgwebaddr.data
        schoolname = form.schoolname.data
        schoolwebaddr = form.schoolwebaddr.data
        pititle = form.pititle.data.title()
        picv = form.picv.data
        pifirstname = form.pifirstname.data.title()
        pimi = form.pimi.data.title()
        pilastname = form.pilastname.data.title()
        pisuffix = form.pisuffix.data.title()
        piemail = form.piemail.data
        pitele = form.pitele.data
        piaddr1 = form.piaddr1.data
        piaddr2 = form.piaddr2.data
        picity = form.picity.data.title()
        pistate = request.form['pistate']
        pizip = form.pizip.data
        othertitle = form.othertitle.data.title() if form.othertitle.data != '' else None
        otherfirstname = form.otherfirstname.data.title() if form.otherfirstname.data != '' else None
        othermi = form.othermi.data.title() if form.othermi.data != '' else None
        otherlastname = form.otherlastname.data.title() if form.otherlastname.data != '' else None
        othersuffix = form.othersuffix.data.title() if form.othersuffix.data != '' else None
        otheremail = form.otheremail.data if form.otheremail.data != '' else None
        othertele = form.othertele.data if form.othertele.data != '' else None
        otheraddr1 = form.otheraddr1.data if form.otheraddr1.data != '' else None
        otheraddr2 = form.otheraddr2.data if form.otheraddr2.data != '' else None
        othercity = form.othercity.data.title() if form.othercity.data != '' else None
        otherstate = request.form['otherstate'] if request.form['otherstate'] != '' else None
        otherzip = form.otherzip.data if form.otherzip.data != '' else None
        irsletter_TF = 0
        budget_TF = 0
        confirmsent_TF = 0
        goal = form.goal.data
        description = form.description.data
        aboutpeople = form.aboutpeople.data if form.aboutpeople.data != '' else None
        relevance = form.relevance.data
        dissemination = form.dissemination.data
        projother = form.projother.data if form.projother.data != '' else None

        crsr.execute("""
            INSERT INTO idea1 (projname,reqamount,newprojnum,orgname,orgwebaddr,schoolname,schoolwebaddr,pititle,picv,pifirstname,pimi,pilastname,pisuffix,piemail,pitele,piaddr1,piaddr2,picity,pistate,pizip,othertitle,otherfirstname,othermi,otherlastname,othersuffix,otheremail,othertele,otheraddr1,otheraddr2,othercity,otherstate,otherzip,irsletter_TF,budget_TF,confirmsent_TF,goal,description,aboutpeople,relevance,dissemination,projother) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                     , (projname, reqamount, None, orgname, orgwebaddr, schoolname, schoolwebaddr, pititle, picv,
                        pifirstname, pimi, pilastname, pisuffix, piemail, pitele, piaddr1, piaddr2, picity, pistate,
                        pizip, othertitle, otherfirstname, othermi, otherlastname, othersuffix, otheremail, othertele,
                        otheraddr1, otheraddr2, othercity, otherstate, otherzip, irsletter_TF, budget_TF,
                        confirmsent_TF, goal, description, aboutpeople, relevance, dissemination, projother)
                     )
        projnum = crsr.lastrowid;

        # update the existing project record with new project number
        crsr.execute("UPDATE idea1 SET newprojnum=%s WHERE projnum=%s", (projnum, existingprojnum))
        conn.commit()

        status = 'success'
        today = date.today()
        msg = "<b>Thank you</b> for sharing your Idea with us.<br><br> \
                We look forward to reading and learning about it.<br><br>\
                Your Project Number is: <b> " + str(projnum) + " </b> <br> <br> \
                Your Submission date is: <b> " + str(today.strftime("%m/%d/%Y")) + " </b> <br> <br> \
                Please save these as they may be required for communicating with us about the project. <br> <br> \
                Because we may use this and other information submitted with your Idea to verfiy persons connected with this project, \
                we suggest you maintain such information securely."

        url = url_for('whatexpect');
        flash(Markup(msg), 'success')
        return jsonify(status=status, data=[], message=msg, url=url)

    return jsonify(status=status, data=form.errors, message='One or more items need revision.  Please modify.')


@bp.route('/send-document', methods=['GET', 'POST'])
def senddocument():
    existingprojnum = ''

    if 'pnum' in request.args:
        existingprojnum = request.args['pnum']
    else:
        flash('Invalid Project', 'error')
        return redirect(url_for('shareidea'))

    today = date.today()
    seconds = str(int(time.time()))
    suffix = today.strftime("%Y-%m-%d") + '-' + seconds

    form = sendDocumentForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            irsfile = form.irsfield.data

            filename = secure_filename(str(existingprojnum) + '-irs-' + suffix + '.' + irsfile.filename.split('.')[1])
            irsfile.save(os.path.join(
                os.getcwd(), 'public', 'static', 'received_files', filename
            ))
            crsr.execute("INSERT INTO myidea_docs (projnum,document) VALUES (%s, %s)", (existingprojnum, filename))

            budfile = form.budfield.data
            filename = secure_filename(str(existingprojnum) + '-bud-' + suffix + '.' + budfile.filename.split('.')[1])
            budfile.save(os.path.join(
                os.getcwd(), 'public', 'static', 'received_files', filename
            ))

            crsr.execute("INSERT INTO myidea_docs (projnum,document) VALUES (%s, %s)", (existingprojnum, filename))

            # update the existing project record with file upload status
            crsr.execute("UPDATE idea1 SET irsletter_TF=1, budget_TF=1 WHERE projnum=%s", (existingprojnum))
            conn.commit()

            flash('Document uploaded successfully.', 'success')
            return redirect(url_for('shareidea'))
        else:
            flash('One or more items is incorrect. Please try with valid files', 'error')

    return render_template('senddocument.html', form=form, existingprojnum=existingprojnum)


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    print("ghjn")
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('security/register_user.html')
