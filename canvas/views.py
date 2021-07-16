from django.shortcuts import render, redirect
from .models import Db, Connection, File
from .forms import BaseForm, FileForm, BusObjForm
import openpyxl as xl
from .constants import (
    X_SPACE,
    new_temp,
    list_temp,
    upload_temp,
    Y_SPACE,
    home_temp,
    home_link,
    home_comment,
    home_header,
    current_y,
    full_name,
    full_name_p,
    ind_template,
    canvas_temp,
)

X_SPACE = 160
Y_SPACE = 70
current_y = 0

full_name = {"role": "Role", "busobj": "Business Objective", "obligation": "Obligation", "theme": "Theme",
             "process": "Process", "risk": "Risk", "metric": "Metric", "control": "Control", "issue": "Issue", }
full_name_p = {"role": "Roles", "busobj": "Business Objectives", "obligation": "Obligations", "theme": "Themes",
             "process": "Processes", "risk": "Risks", "metric": "Metrics", "control": "Controls", "issue": "Issues", }
ind_template = {"role": "ind_role", "busobj": "ind", "obligation": "ind", "theme": "ind",
             "process": "ind", "risk": "ind", "metric": "ind", "control": "ind", "issue": "ind", }

def home(request):
    header = home_header
    comment = home_comment
    link = home_link
    link_desc = "Description"
    return render(
        request,
        home_temp,
        {"header": header, "comment": comment, "link": link, "link_desc": link_desc},
    )


def set_loc_layer(type):
    global current_y
    for level in range(1, 7):
        this_row = Db.objects.filter(type=type, level=level)
        if this_row.count() > 0:
            current_x = int(
                20 + X_SPACE * 3 - (min(this_row.count(), 7) - 1) / 2 * X_SPACE
            )
            for item in this_row:
                item.y = current_y
                item.x = current_x
                item.save()
                current_x += X_SPACE
                if current_x >= X_SPACE * 7:
                    current_x = int(20)
                    current_y += Y_SPACE / 2

            current_y += Y_SPACE


def set_locations():
    global current_y
    current_y = 50
    set_loc_layer("role")
    set_loc_layer("busobj")
    set_loc_layer("obligation")
    set_loc_layer("theme")
    set_loc_layer("process")
    set_loc_layer("risk")
    set_loc_layer("metric")
    set_loc_layer("control")
    set_loc_layer("issue")


def map(request, type, id):
    Connection.objects.all().delete()
    db = Db.objects.all()
    db.update(visible=False)
    first = Db.objects.get(id=id)
    first.visible = True
    first.save()
    for item in db:
        for item2 in item.links.all():
            if item.level <= item2.level:
                new = Connection(a=item, b=item2)
                if item.visible:
                    print(item, item2)
                    item2.visible = True
                    item2.save()
                    new.visible = True
                new.save()
    connections = Connection.objects.all()
    set_locations()

    return render(request, canvas_temp, {"nodes": db, "connections": connections})


def ind(request, type, id):
    messages=[]
    template = ind_template[type] + ".html"
    item = Db.objects.get(pk=id)
    objects = item.links.all()
    owners = objects.filter(type="role")
    busobjs = objects.filter(type="busobj")
    processes = objects.filter(type="process")
    risks = objects.filter(type="risks")

    busobj_form = BusObjForm(request.POST or None, instance=item)

    if type == "role":
        for x in busobjs:
            processes = processes | x.links.all().filter(type="process")
            risks = risks | x.links.all().filter(type="risk")
            x.visible = True
            x.save()
        for x in processes:
            risks = risks | x.links.all().filter(type="risk")
            print(x, x.links.filter(type="risk"))

        if busobj_form.is_valid():
            busobj_form.save()
        first = Db.objects.get(id=id)
        if busobjs.count() == 0:
            messages.append("You currently have no business objectives. Consider adding some.")
        for busobj in busobjs:
            item_processes = busobj.links.all().filter(type="process").count()
            if item_processes == 0: messages.append(f"Your business objective '{busobj}' has no processes. Consider adding some.")

        db = Db.objects.all()
        db.update(visible=False)
        first.x = 50
        first.y = 50
        first.save()

    processes = processes.distinct()

    return render(request, template, {'item': item, 'type': type, 'owners': owners,'busobj_form':busobj_form,
                                      'busobjs':busobjs, 'nodes': busobjs, 'processes':processes,'risks':risks,
                                      'messages':messages})

def update(request, type, id):
    item = Db.objects.get(pk=id)
    form = BaseForm(request.POST or None, instance=item)
    # if type == "risk":
    #     form = RiskForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/list/' + type)
    header = full_name[type] + ": " + item.name
    processes = item.links.all().filter(type="process")
    return render(request, 'update.html', {'header': header,'item': item, 'form': form, 'type': type})

def list(request, type):
    header = full_name_p[type]
    new_link = type + "_new"
    list = Db.objects.filter(type=type)
    return render(
        request,
        list_temp,
        {"header": header, "type": type, "new_link": new_link, "list": list},
    )


def new(request, type):
    header = "New " + full_name[type]
    if request.method == "POST":
        form = BaseForm(request.POST)
        # if type == "risk":
        #     form = RiskForm(request.POST)
        if form.is_valid():
            new = form.save()
            new.type = type
            form.save()
            return redirect("/list/" + type)
    else:
        form = BaseForm()
        # if type == "risk":
        #     form = RiskForm()
    return render(request, new_temp, {"header": header, "form": form})

def delete(request, type, id):
    item = Db.objects.get(pk=id)
    item.delete()
    return redirect("/list/" + type)


def upload(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save()
            if new_file.name.find("Report") != -1:
                new_file.type = "Report Template"
            form.save()
            return redirect("files")
    else:
        form = FileForm()
    return render(request, upload_temp, {"form": form})


def load(request, type, id):
    file = File.objects.filter(id=id)[0]
    path = str(file.document.url)[1:]
    messages = []
    try:
        wb = xl.load_workbook(path)
    except:
        header = full_name_p[type]
        new_link = type + "_new"
        list = Db.objects.filter(type=type)
        message = f"Could not find {file} in {path}"
        messages.append(message)
        return render(
            request,
            list_temp,
            {"header": header, "type": type, "new_link": new_link, "list": list},
        )

    sheet = wb.active
    for row in range(2, sheet.max_row + 1):
        name = sheet.cell(row, 1).value
        role = sheet.cell(row, 2).value
        parent_role = sheet.cell(row, 3).value
        level = 1

        if Db.objects.filter(name=parent_role).count() > 0:
            parent_object = Db.objects.filter(name=parent_role)[0]
            level = parent_object.level + 1
        else:
            parent_object = None
            messages.append(f"No parent found for {name}")

        if Db.objects.filter(name=role).count() == 0 and role is not None:
            new_role = Db(name=role, incumbant=name, level=level, type=type)
            new_role.save()
            if parent_object is not None:
                new_role.links.add(parent_object)
            new_role.save()

    return redirect("/list/" + type)


def files(request):
    list = File.objects.all().order_by("type")
    return render(request, "files.html", {"list": list})


def file_delete(request, id):
    if request.method == "POST":
        file = File.objects.get(pk=id)
        file.delete()
    return redirect("files")


# TODO Show details of selected nodes
# TODO Add a join button
# TODO Allow join selection (to edit strength or delete)
# TODO change size to fit on page
# TODO allow user to start from one node
