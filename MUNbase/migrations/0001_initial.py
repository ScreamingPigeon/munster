# Generated by Django 3.2.5 on 2021-08-15 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now=True)),
                ('content', models.CharField(max_length=20000)),
                ('author', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=2000)),
                ('countrylist', models.CharField(blank=True, max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Motion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('proposer', models.CharField(max_length=100)),
                ('yes', models.CharField(default='0', max_length=10)),
                ('no', models.CharField(default='0', max_length=10)),
                ('abstain', models.CharField(default='0', max_length=10)),
                ('committee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MUNbase.committee')),
            ],
        ),
        migrations.CreateModel(
            name='MUNuser',
            fields=[
                ('id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=50)),
                ('email', models.CharField(default=None, max_length=50)),
                ('username', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=100)),
                ('institution', models.CharField(default='', max_length=50)),
                ('number', models.CharField(default='+91 ', max_length=15)),
                ('description', models.CharField(default='', max_length=300)),
                ('url', models.CharField(default='http://', max_length=200)),
                ('city', models.CharField(default='', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('secondname', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=100)),
                ('contactnum', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=20)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.committee')),
            ],
        ),
        migrations.CreateModel(
            name='Talklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('secsps', models.CharField(blank=True, max_length=10, null=True)),
                ('numberofspeakers', models.CharField(default=0, max_length=100)),
                ('active', models.CharField(default='N', max_length=1)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.committee')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(default=None, max_length=50)),
                ('email', models.CharField(default=None, max_length=50)),
                ('username', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=100)),
                ('institution', models.CharField(default='', max_length=50)),
                ('age', models.IntegerField(default=0)),
                ('city', models.CharField(default='', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.CharField(default='NV', max_length=10)),
                ('motion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.motion')),
                ('voter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MUNbase.participant')),
            ],
        ),
        migrations.CreateModel(
            name='TalkListSpeaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timespent', models.CharField(default=0, max_length=3)),
                ('status', models.CharField(default='qd', max_length=10)),
                ('time', models.DateField(auto_now=True)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.talklist')),
                ('speaker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.participant')),
            ],
        ),
        migrations.CreateModel(
            name='Registrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MUN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.munuser')),
                ('delegate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.user')),
            ],
        ),
        migrations.CreateModel(
            name='Paperwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=1000)),
                ('body', models.TextField(default='')),
                ('mainsubmitter', models.CharField(max_length=1000)),
                ('time', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='QUE', max_length=10)),
                ('committee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MUNbase.committee')),
            ],
        ),
        migrations.CreateModel(
            name='MUNwatchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delegate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.user')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.munuser')),
            ],
        ),
        migrations.CreateModel(
            name='MUNannouncements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=300)),
                ('dateofcreation', models.DateField(auto_now=True)),
                ('announcer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.munuser')),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MUN', models.CharField(default='', max_length=50)),
                ('committee', models.CharField(default='', max_length=50)),
                ('year', models.IntegerField(default=2020)),
                ('position', models.CharField(default='', max_length=20)),
                ('delegate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.user')),
            ],
        ),
        migrations.CreateModel(
            name='Delwatchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delegate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='MUNbase.user')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='MUNbase.user')),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=50)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.committee')),
            ],
        ),
        migrations.AddField(
            model_name='committee',
            name='mun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MUNbase.munuser'),
        ),
        migrations.CreateModel(
            name='Ammendment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clause', models.CharField(default='', max_length=5)),
                ('proposer', models.CharField(default='', max_length=100)),
                ('type', models.CharField(default='Addition', max_length=100)),
                ('content', models.TextField(default='')),
                ('status', models.CharField(default='QUE', max_length=10)),
                ('time', models.DateTimeField(auto_now=True)),
                ('paperwork', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MUNbase.paperwork')),
            ],
        ),
    ]
