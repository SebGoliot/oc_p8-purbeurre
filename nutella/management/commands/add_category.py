from django.core.management.base import BaseCommand, CommandError
from nutella.models import Category
from django.db.utils import OperationalError

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'category_name',
            nargs='+',
            type=str, 
            help="The name of the category to add"
        )


    def handle(self, *args, **options):
        category_name = ' '.join(options['category_name'])

        if self._name_is_available(category_name):
            category = Category(name=category_name)
            category.save()

            self.stdout.write(self.style.SUCCESS(
                f"Successfuly created a new category: {category_name}"
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f"Looks like this category already exist: {category_name}"
            ))
        
        self.stdout.write(self.style.NOTICE(
            "Please use `manage.py update_db` to populate this category"
        ))


    def _name_is_available(self, category_name:str) -> bool:
        """Checks if the category_name is available

        Args:
            category_name (str): The name of the category to check

        Returns:
            bool: Returns True if the name is avalable, else False
        """
        try:
            free = not Category.objects.filter(name = category_name).exists()
        except OperationalError as err:
            self.stdout.write(self.style.ERROR(
                f"Could not create the category `{category_name}` !\n{err}"
            ))
            return False
        return free
