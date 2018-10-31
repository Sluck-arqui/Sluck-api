import json
import random
from django.db import transaction
from sluck_api.models import (
    User,
    Group,
    Hashtag,
    Message,
    ThreadMessage,
    MessageReaction,
    ThreadMessageReaction,
)
from faker import Faker


N_USERS = 10
N_MESSAGES_PER_USER = 5
N_THREADS_PER_USER = 1
N_LIKES_PER_USER = 3
N_DISLIKES_PER_USER = 2
N_THREAD_LIKES_PER_USER = 3
N_THREAD_DISLIKES_PER_USER = 4


@transaction.atomic
def load():
    fake = Faker('es_ES')

    # PUBLIC GROUP
    public_group = Group.objects.create(
        name="General",
        description="Grupo general para todos los usuarios",
    )

    users = []
    messages = []
    threads = []

    for i in range(N_USERS):
        first_name = fake.first_name()
        user = User.objects.create(
            username=f"{first_name}{i}",
            first_name=first_name,
            last_name=fake.last_name(),
            password="password",
            email=fake.email()
        )
        user.save()
        user.groups.add(public_group)
        users.append(user)
        for _ in range(N_MESSAGES_PER_USER):
            message = Message.objects.create(
                text=fake.text(),
                author=user,
                group=public_group,
            )
            message.publish()
            messages.append(message)

    for user in users:
        for _ in range(N_LIKES_PER_USER):
            message = random.choice(messages)
            MessageReaction(author=user, message=message,
                            reaction_type=1).save()
        for _ in range(N_DISLIKES_PER_USER):
            message = random.choice(messages)
            MessageReaction(author=user, message=message,
                            reaction_type=0).save()
        for _ in range(N_THREADS_PER_USER):
            message = random.choice(messages)
            thread = ThreadMessage.objects.create(
                text=fake.text(),
                author=user,
                message=message,
            )
            threads.append(thread)

    for user in users:
        for _ in range(N_THREAD_LIKES_PER_USER):
            thread = random.choice(threads)
            ThreadMessageReaction(author=user, thread=thread,
                                  reaction_type=1).save()
        for _ in range(N_THREAD_DISLIKES_PER_USER):
            thread = random.choice(threads)
            ThreadMessageReaction(author=user, thread=thread,
                                  reaction_type=1).save()


load()
