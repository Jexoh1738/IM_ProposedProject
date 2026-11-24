from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.surveys.queries import answers_with_details, checkins_with_reported_discomfort


class Command(BaseCommand):
    help = "Print the SQL that Django generates for the JOIN and SUBQUERY implementations"

    def add_arguments(self, parser):
        parser.add_argument("--user-id", type=int, help="user to build the queries for (default: first user)")

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.filter(pk=options["user_id"]).first() if options["user_id"] else User.objects.first()
        if user is None:
            self.stderr.write("No users found. Register an account first.")
            return

        self.show("JOIN", answers_with_details(user), user)
        self.show("SUBQUERY", checkins_with_reported_discomfort(user), user)

    def show(self, title, queryset, user):
        # sql_with_params() is exact: str(queryset.query) leaves string parameters unquoted
        # (it would print  value = true  although Django really sends the text 'true').
        sql, params = queryset.query.sql_with_params()
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n== {title} (user id {user.pk}) =="))
        self.stdout.write(sql)
        self.stdout.write(f"-- parameters: {params}\n")
