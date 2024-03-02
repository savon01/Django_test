from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Product, Group, Student
from .forms import RegistrationForm
from django.db.models import Count


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shopapp/product_list.html', {'products': products})


class RegisterView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = RegistrationForm()
        return render(request, 'shopapp/register.html', {'product': product, 'form': form})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            paid = form.cleaned_data['paid']
            group = self.get_group_for_registration(product)
            student = Student.objects.create(first_name=first_name, last_name=last_name, phone=phone, paid=paid, group=group)
            return redirect('shopapp:product_list')

        return render(request, 'shopapp/register.html', {'product': product, 'form': form})

    def get_group_for_registration(self, product):
        groups = product.groups.annotate(num_students=Count('students'))
        min_group_size = product.min_students_per_group
        max_group_size = product.max_students_per_group

        available_groups = []
        for group in groups:
            if group.num_students < max_group_size:
                available_groups.append(group)

        sorted_groups = sorted(available_groups, key=lambda x: (x.num_students, x.id))

        for group in sorted_groups:
            if group.num_students < min_group_size or group.num_students < max_group_size:
                return group

        new_group = Group.objects.create(product=product, name=f"Group {groups.count() + 1}")
        return new_group



