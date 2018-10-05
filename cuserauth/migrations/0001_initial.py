# Generated by Django 2.1.2 on 2018-10-05 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cfrom', models.TimeField()),
                ('cto', models.TimeField()),
                ('date', models.DateField()),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('adress', models.CharField(max_length=200)),
                ('college_id', models.CharField(max_length=200, unique=True)),
                ('ld_phone', models.CharField(max_length=20)),
                ('sub_start', models.DateTimeField(blank=True)),
                ('sub_end', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cource_id', models.CharField(default='None', max_length=200)),
                ('domain', models.CharField(max_length=200)),
                ('year', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Incharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=200)),
                ('user_name', models.CharField(default='None', max_length=200, unique=True)),
                ('password', models.CharField(default='password', max_length=200)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cuserauth.College')),
            ],
        ),
        migrations.CreateModel(
            name='Offerd_course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(blank=True)),
                ('end', models.DateTimeField(blank=True)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuserauth.College')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuserauth.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=5)),
                ('year', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuserauth.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=200)),
                ('parent', models.CharField(max_length=200)),
                ('phones', models.CharField(max_length=200)),
                ('roll_no', models.CharField(max_length=200, unique=True)),
                ('year', models.IntegerField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cuserauth.College')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cuserauth.Course')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cuserauth.Section')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=200)),
                ('year', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuserauth.Course')),
            ],
        ),
        migrations.AddField(
            model_name='incharge',
            name='sec',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cuserauth.Section'),
        ),
        migrations.AddField(
            model_name='incharge',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cuserauth.Subjects'),
        ),
        migrations.AddField(
            model_name='attendence',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cuserauth.Students'),
        ),
        migrations.AddField(
            model_name='attendence',
            name='subject_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cuserauth.Subjects'),
        ),
    ]
