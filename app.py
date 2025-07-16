from app import create_app, db
from app.models import User, News, Event, RSVP, Job, Testimonial, ContactSubmission
from app.utils.helpers import init_app as init_helpers

app = create_app()
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