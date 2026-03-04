from django.core.management.base import BaseCommand

from patients.models.patientvisit_models import PostVisitOption


class Command(BaseCommand):
    help = "Creates initial PostVisitOption items"

    def handle(self, *args, **options):
        POST_VISIT_CHOICES = [
            'Lab', 'Referral', 'Treatment', 'Dentist Report'
        ]

        created_count = 0
        for choice in POST_VISIT_CHOICES:
            # get_or_create prevents errors if the command runs twice
            obj, created = PostVisitOption.objects.get_or_create(name=choice)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created: {choice}'))
                created_count += 1
            else:
                self.stdout.write(f'Already exists: {choice}')

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {created_count} items.'))
