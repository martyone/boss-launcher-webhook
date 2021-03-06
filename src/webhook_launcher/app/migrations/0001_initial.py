# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-14 12:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namespace', models.CharField(help_text=b'This is also used to identify the OBS alias in BOSS processes', max_length=50, unique=True)),
                ('apiurl', models.CharField(max_length=250, unique=True)),
                ('weburl', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LastSeenRevision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.CharField(max_length=250)),
                ('tag', models.CharField(blank=True, max_length=50, null=True)),
                ('handled', models.BooleanField(default=False, editable=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('emails', models.TextField(blank=True, editable=False, null=True)),
                ('payload', models.TextField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=b'The OBS project name. eg nemo:mw', max_length=250)),
                ('official', models.BooleanField(default=True, help_text=b'If set then only valid namespaces can be used for the git repo')),
                ('allowed', models.BooleanField(default=True, help_text=b'If not set then webhooks are not allowed for this project. This is useful for projects which should only have specific versions of packages promoted to them.')),
                ('gated', models.BooleanField(default=False, help_text=b'If set then webhooks pointing at this project will be triggered to a side project instead and then an autopromotion attempted. This is useful for projects which apply formal entry checks and/or QA.')),
                ('match', models.CharField(blank=True, help_text=b'If set then used as well as name to re.match() project names', max_length=250, null=True)),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group')),
                ('obs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BuildService')),
            ],
        ),
        migrations.CreateModel(
            name='QueuePeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(default=django.utils.timezone.now)),
                ('end_time', models.TimeField(default=django.utils.timezone.now)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('recurring', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('projects', models.ManyToManyField(to='app.Project')),
            ],
            options={
                'permissions': (('can_override_queueperiod', 'Can override queue periods'),),
            },
        ),
        migrations.CreateModel(
            name='RelayTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text=b'Whether this relay will fire on matching events')),
                ('name', models.CharField(help_text=b'Friendly name of recipient, for example: Organization name', max_length=50)),
                ('url', models.CharField(help_text=b'HTTP(S) endpoint which will receive POST of GIT events (for example http://webhook.example.com/webhook/)', max_length=200)),
                ('verify_SSL', models.BooleanField(default=True, help_text=b'Turn on SSL certificate verification')),
            ],
        ),
        migrations.CreateModel(
            name='VCSNameSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(help_text=b'the network path (gitlab group or github organization eg. /mer-core)', max_length=200)),
                ('default_project', models.ForeignKey(blank=True, help_text=b'Default project for webhook placeholder creation', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Project')),
            ],
        ),
        migrations.CreateModel(
            name='VCSService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text=b'Friendly name of this VCS hosting service', max_length=50, unique=True)),
                ('netloc', models.CharField(help_text=b'Network location from payload (for example: git@git.merproject.org:1234)', max_length=200, unique=True)),
                ('ips', models.TextField(blank=True, help_text=b'Known IP adresses of this service (optional)', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WebHookMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repourl', models.CharField(help_text=b'url of git repo to clone from. Should be a remote http[s]', max_length=200)),
                ('branch', models.CharField(default=b'master', help_text=b'name of branch to use. If not specified default branch (or currently checked out one) will be used', max_length=100)),
                ('project', models.CharField(default=b'', help_text=b'name of an existing project under which to create or update the package', max_length=250)),
                ('package', models.CharField(help_text=b'name of the package to create or update in OBS', max_length=250)),
                ('token', models.CharField(blank=True, default=b'', help_text=b'a token that should exist in tag names and changelog entry headers to enable handling them', max_length=100, null=True)),
                ('debian', models.CharField(blank=True, choices=[(b'N', b'N'), (b'Y', b'Y')], default=b'', help_text=b'Choose Y to turn on debian packaging support', max_length=2, null=True)),
                ('dumb', models.CharField(blank=True, choices=[(b'N', b'N'), (b'Y', b'Y')], default=b'', help_text=b'Choose Y to take content of revision as-is without automatic processing (example: tarballs in git)', max_length=2, null=True)),
                ('notify', models.BooleanField(default=True, help_text=b'Enable IRC notifications of events')),
                ('build', models.BooleanField(default=True, help_text=b'Enable OBS build triggering')),
                ('comment', models.TextField(blank=True, default=b'', null=True)),
                ('obs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BuildService')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='vcsnamespace',
            name='service',
            field=models.ForeignKey(help_text=b'VCS service where this namespace is hosted', on_delete=django.db.models.deletion.CASCADE, to='app.VCSService'),
        ),
        migrations.AddField(
            model_name='relaytarget',
            name='sources',
            field=models.ManyToManyField(help_text=b'List of VCS namespaces (for example github organization or gitlab groups)', to='app.VCSNameSpace'),
        ),
        migrations.AddField(
            model_name='project',
            name='vcsnamespaces',
            field=models.ManyToManyField(blank=True, to='app.VCSNameSpace'),
        ),
        migrations.AddField(
            model_name='lastseenrevision',
            name='mapping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.WebHookMapping'),
        ),
        migrations.AlterUniqueTogether(
            name='webhookmapping',
            unique_together=set([('project', 'package', 'obs')]),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('name', 'obs')]),
        ),
    ]
