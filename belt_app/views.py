from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages
import bcrypt


def index(req):
    return render(req, 'index.html')


def register(req):
    print(req.POST)
    errors = User.objects.regValidator(req.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(req, value)
        return redirect("/")
    else:
        pw_hash = bcrypt.hashpw(
            req.POST['pw'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(
            first_name=req.POST['first_name'], last_name=req.POST['last_name'], email=req.POST['email'], password=pw_hash)
        req.session['logged_in_id'] = newUser.id
        return redirect("/quotes")


def login(req):
    print(req.POST)
    errors = User.objects.loginValidator(req.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(req, value)
        return redirect("/")
    else:
        email_filter = User.objects.filter(
            email=req.POST['email'])
        req.session['logged_in_id'] = email_filter[0].id
        return redirect("/quotes")


def logout(req):
    req.session.clear()
    return redirect("/")


def quotes(req):
    if 'logged_in_id' not in req.session:
        messages.error(req, "You must log in to see the dashboard.")
        return redirect("/")
    context = {
        'logged_in_user': User.objects.get(id=req.session['logged_in_id']),
        'all_quotes': Quote.objects.all()
    }
    return render(req, 'quotes.html', context)


def add_quote(req):
    errors = Quote.objects.quoteValidator(req.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(req, value)
        return redirect("/quotes")

    new_quote = Quote.objects.create(author=req.POST['author'], content=req.POST['quote_content'], uploader=User.objects.get(
        id=req.session['logged_in_id']))
    return redirect("/quotes")


def delete_quote(req, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.delete()
    return redirect("/quotes")


def like_quote(req, quote_id):
    user = User.objects.get(id=req.session['logged_in_id'])
    quote = Quote.objects.get(id=quote_id)
    quote.likes.add(user)
    return redirect("/quotes")


def show_user(req, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(req, "show_user.html", context)


def edit_acct(req, user_id):
    context = {
        'logged_in_user': User.objects.get(id=req.session['logged_in_id']),
    }
    return render(req, 'edit_acct.html', context)


def make_changes(req, user_id):
    errors = User.objects.updateValidator(req.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(req, value)
        return redirect(f"/myaccount/{user_id}")

    updated_user = User.objects.get(id=user_id)
    updated_user.first_name = req.POST['first_name']
    updated_user.last_name = req.POST['last_name']
    updated_user.email = req.POST['email']
    updated_user.save()

    return redirect("/quotes")
