from app import create_app, db,mail
from flask_mail import Message
from app.models import User, News, Event, RSVP, Job, Testimonial, ContactSubmission
from app.utils.helpers import init_app as init_helpers

app = create_app()
with app.app_context():
    msg = Message('Test Email', sender='groupimak@gmail.com', recipients=['test@example.com'], body='Test')
    try:
        mail.send(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Email error: {str(e)}")
init_helpers(app)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'News': News,
        'Event': Event,
        'RSVP': RSVP,
        'Job': Job,
        'Testimonial': Testimonial,
        'ContactSubmission': ContactSubmission
    }

if __name__ == '__main__':
    app.run(debug=True)