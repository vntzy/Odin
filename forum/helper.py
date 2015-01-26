from django.core.mail import send_mass_mail
from django.conf import settings

from forum.models import Comment
from students.models import User


def send_topic_subscribe_email(topic, comment):
    users = User.objects.filter(subscribed_topics=topic)
    emails = []
    for user in users:
        if comment.author != user:
            message = open(
                settings.BASE_DIR + '/forum/templates/email/send_topic_subscribe_email.txt', encoding='utf-8').read()

            message = message.format(
                name=user.get_full_name(),
                domain=settings.DOMAIN,
                topic=topic.id,
                comment=comment.id
            )

            emails.append((
                'Hack Bulgaria new comment in "{0}"'.format(topic.title),
                message,
                settings.DEFAULT_FROM_EMAIL,
                (user.email,)
            ))

    send_mass_mail(emails)


def subscribe_to_topic(user, topic):
    users_comments_for_topic = Comment.objects.filter(author=user, topic=topic).count()

    # Checking if this is the first comment
    if users_comments_for_topic <= 1:
        user.subscribed_topics.add(topic)
        user.save()
