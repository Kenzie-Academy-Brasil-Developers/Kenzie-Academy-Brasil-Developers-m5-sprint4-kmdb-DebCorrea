# Generated by Django 4.1.2 on 2022-10-18 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0002_rename_user_review_critic_alter_review_stars"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="recommendation",
            new_name="recomendation",
        ),
    ]