from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render ,redirect
from django.db.models import Q
from django.db.models import Count
from .models import Topic, About, Lead
from .forms import LeadForm, TopicForm, AboutForm, CSVUploadForm
import csv
from django.http import HttpResponse

def superuser_required(user):
    return user.is_authenticated and user.is_superuser

def home(request):
    project = About.objects.get(id=1)
    context = {'project':project}
    return render(request, 'crm/home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('leads')

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('leads')

    return render(request, 'crm/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'crm/register.html', {'form': form})

@login_required(login_url='home')
def leads_view(request):
    sq = request.GET.get('sq') if request.GET.get('sq') != None else ''
    leads = Lead.objects.filter(user=request.user)

    if sq !='':
        leads = leads.filter(
            Q(topic__name__icontains=sq) |
            Q(name__icontains=sq) |
            Q(email__icontains=sq) |
            Q(phone__icontains=sq) |
            Q(description__icontains=sq))
        

    context = {'leads':leads, }
    return render(request, 'crm/leads.html', context)



@login_required(login_url='home')
def add_lead(request):
    form = LeadForm(user=request.user)
    form1 = CSVUploadForm()

    if request.method == 'POST':
        if 'Upload CSV' in request.POST:
            form1 = CSVUploadForm(request.POST, request.FILES)
            if form1.is_valid():
                csv_file = request.FILES['csv_file']
                handle_uploaded_csv(csv_file, request.user)
                return redirect('leads')

        elif 'submit' in request.POST:
            form = LeadForm(request.POST, user=request.user)
            if form.is_valid():
                # Save the form with the user
                lead = form.save(commit=False)
                lead.user = request.user
                lead.save()
                return redirect('leads')

    context = {'form': form, 'form1': form1}
    return render(request, 'crm/add_edit_leads.html', context)

def handle_uploaded_csv(csv_file, user_name):
    # Process the CSV file and populate the database
    reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
    for row in reader:
        topic_name = row['Topic']
        topic, created = Topic.objects.get_or_create(user=user_name, name=topic_name)

        Lead.objects.create(
            user=user_name,
            topic=topic,
            name=row['Name'],
            email=row['Email'],
            phone=row['Phone'],
            description=row['Description'],
            
        )

@login_required(login_url='home')
def delete_lead(request, pk):
    leads = Lead.objects.get(id=pk)
    if request.method == 'POST':
        leads.delete()
        return redirect('leads')
    return render(request, 'crm/delete.html', {'obj':leads})

@login_required(login_url='home')
def edit_lead(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm(instance=lead, user=request.user)
    form1 = CSVUploadForm()
    
    if request.method == 'POST':
        if 'Upload CSV' in request.POST:
            form1 = CSVUploadForm(request.POST, request.FILES)
            if form1.is_valid():
                csv_file = request.FILES['csv_file']
                handle_uploaded_csv(csv_file, request.user)
                return redirect('leads')

        elif 'submit' in request.POST:
            form = LeadForm(request.POST, instance=lead, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('leads')

    context = {'form': form, 'form1': form1, 'lead': lead}
    return render(request, 'crm/add_edit_leads.html', context)

@login_required(login_url='home')
def add_remove_topic(request):
    topics = Topic.objects.filter(user=request.user)
    form = TopicForm()

    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            # Save the form with the user
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            return redirect('topic')
    context = {'topics':topics, 'form': form}
    return render(request, 'crm/topic.html', context)

@login_required(login_url='home')
def delete_topic(request, pk):
    topics = Topic.objects.get(id=pk)
    if request.method == 'POST':
        topics.delete()
        return redirect('topic')
    return render(request, 'crm/delete.html', {'obj':topics})

@login_required(login_url='home')
def download_csv(request):
    sq = request.GET.get('sq') if request.GET.get('sq') != None else ''
    leads = Lead.objects.filter(user=request.user)
    topics = Topic.objects.filter(user=request.user)
    if sq !='':
        leads = leads.filter(
            Q(topic__name__icontains=sq) |
            Q(name__icontains=sq) |
            Q(email__icontains=sq) |
            Q(phone__icontains=sq) |
            Q(description__icontains=sq))

    # Create a response object with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="leads.csv"'

    # Create a CSV writer and write the header
    csv_writer = csv.writer(response)
    csv_writer.writerow(['Topic', 'Name', 'Email', 'Phone', 'Description'])

    # Write lead data to the CSV file
    for lead in leads:
        csv_writer.writerow([lead.topic.name, lead.name, lead.email, lead.phone, lead.description])

    return response

@user_passes_test(superuser_required)
def superuser_admin(request):
    project = About.objects.get(id=1)
    form = AboutForm(instance=project)

    if request.method == 'POST':
        form = AboutForm(request.POST, instance=project)
        if form.is_valid():
            project.save()
            return redirect('home')

    context = {'project':project, 'form':form}
    return render(request, 'crm/superuser_home.html', context)

@user_passes_test(superuser_required)
def superuser_users(request):
    users = User.objects.count()
    topics = Topic.objects.count()
    leads = Lead.objects.count()
    user_topics_counts = User.objects.annotate(num_topics=Count('topic', distinct=True), num_leads=Count('lead', distinct=True))

    context = {'users':users, 'topics':topics, 'leads':leads, 'user_topics_counts':user_topics_counts}
    return render(request, 'crm/superuser_users.html', context)

@user_passes_test(superuser_required)
def delete_user(request, pk):
    users = User.objects.get(id=pk)
    if request.method == 'POST':
        users.delete()
        return redirect('superuser_users')
    return render(request, 'crm/delete.html', {'obj':users})

@user_passes_test(superuser_required)
def superuser_topic(request, pk):
    users = User.objects.get(id=pk)
    topics = Topic.objects.filter(user=users.id)

    if request.method == 'POST':
        is_superuser = request.POST.get('is_superuser')
        users.is_superuser = is_superuser == 'on'
        users.save()
        return redirect('superuser_topic', pk=users.id)

    context = {'users':users, 'topics':topics}
    return render(request, 'crm/superuser_topics.html', context)

@user_passes_test(superuser_required)
def superuser_leads(request, pk):
    users = User.objects.get(id=pk)
    leads = Lead.objects.filter(user=users.id)

    if request.method == 'POST':
        is_superuser = request.POST.get('is_superuser')
        users.is_superuser = is_superuser == 'on'
        users.save()
        return redirect('superuser_leads', pk=users.id)

    context = {'users':users, 'leads':leads}
    return render(request, 'crm/superuser_leads.html', context)