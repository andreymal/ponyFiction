from optparse import make_option
from django.core.management.base import BaseCommand
from django.db import transaction
from ...models import Story


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--rating-only',
            action = 'store_true',
            dest = 'rating_only',
            default = False,
        ),
    )

    @transaction.commit_manually
    def handle(self, *args, **options):
        try:
            for i, story in enumerate(Story.objects.all()):
                story.update_rating(rating_only = options['rating_only'])
                if i%100 == 0: transaction.commit()
            transaction.commit()
        except:
            transaction.rollback()
            raise