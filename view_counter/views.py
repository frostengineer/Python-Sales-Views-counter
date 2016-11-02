from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,Http404
from view_counter.forms import Posted_SaleForm, UserForm
from view_counter.models import Posted_Sale, View_Count
from django.contrib.auth import authenticate, login
# Create your views here

def login_user(request):
	if not request.user.is_authenticated():
		if request.method == 'POST':
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect('/')
				else:
					return HttpResponse("Your Users account is disabled.")
			else:
				print "Invalid login details: {0}, {1}".format(username, password)
				return HttpResponse("Invalid login details supplied.")
		else:
			return render(request,'login.html', {})
	else:
		return HttpResponseRedirect('/');
	
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render(request,
            'register.html',
            {'user_form': user_form,'registered': registered})
	
def index(request):
	if request.user.is_authenticated():
		query = Posted_Sale.objects.filter(user= request.user)
		return render(request,'index.html', {"query":query})
	else:
		return HttpResponseRedirect('/login');

def create_sale(request,sale_id):
	if request.user.is_authenticated():
		view_id = None
		if sale_id:
				try:
					view_id = Posted_Sale.objects.get(id=sale_id)
				except Posted_Sale.DoesNotExist:
					return Http404('This Sales do not Exist!')
				if request.user.id != view_id.user.id:
					return HttpResponseRedirect('/view_sale/'+str(sale_id)) # just redirecting the non author to view page
		if request.method == 'POST':
			form = Posted_SaleForm (request.POST,instance = view_id)
			if form.is_valid():
				sale_form =form.save(commit = False)
				sale_form.user=request.user
				sale_form.save()
				return HttpResponseRedirect('/')
		else:
			sale_form = Posted_SaleForm(instance = view_id)
			
		return render(request,'create_sale.html',{'sale_form':sale_form, 'sale_id':sale_id})
	else:
		return HttpResponseRedirect('/login');

def view_sale(request,vid):
	if request.user.is_authenticated():
		context = {}
		if vid:
			try:
				view_id = Posted_Sale.objects.get(id=vid)
				edit = False
				if request.user.id == view_id.user.id:
					edit = True
				views_info = View_Count(sale=view_id, user=request.user)
				context['view_id'] = view_id
				context.update( views_info.save() ) # we add counter of view and name of users seen this post, thanks to customised self.save method!
				context['edit'] =edit;
			except:
				print "Sale doesnt exist"
				
		else:
			all_sales = Posted_Sale.objects.all()
			context['all_sales'] = all_sales
		return render(request,"view_sale.html", context)
	else:
		 return HttpResponseRedirect('/login');

