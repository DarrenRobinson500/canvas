from django.shortcuts import render, redirect
from .models import BusObj, Process, Node, Connection
from .forms import BusObjForm, ProcessForm

X_SPACE = 160
Y_SPACE = 50

full_name = {"busobj": "Business Objective", "process": "Process"}
full_name_p = {"busobj": "Business Objectives", "process": "Processes"}
ind_file = {"busobj": "ind", "process": "ind"}

def home(request):
    header = "Business Objectives"
    comment = "You currently have no business objectives"
    link = "busobj_new"
    link_desc = "New Business Objective"
    return render(request, 'home.html', {'header': header, 'comment': comment, 'link': link, 'link_desc': link_desc})

def add_child(child,node):
    new_node = Node(level=child.level, text=child.name, description=child.description)
    new_node.save()
    new_node.parent.add(node)
    if child.level <= 3:
        new_node.busobj = child
    elif child.level <= 6:
        new_node.process = child
    new_node.save()
    if child.level <= 5:
        add_children(new_node, new_node.level + 1)

def add_children(node, level):
    if level <= 3:
        item = node.busobj
    elif level <= 6:
        item = node.process
    if item is not None:
        children = BusObj.objects.filter(parent__id=item.id).filter(level__gte=level)
        for child in children: add_child(child, node)

        children = Process.objects.filter(parent__id=item.id).filter(level__gte=level)
        print(node, children, Process.objects.filter(parent__id=item.id), level)
        for child in children:
            add_child(child, node)

        if level <= 3:
            children = item.process_set.all()
            for child in children: add_child(child, node)

        children_nodes = Node.objects.filter(parent=node)
        count = 0
        for child_node in children_nodes:
            child_node.y = int(-(children_nodes.count()-1)/2 * Y_SPACE + count * Y_SPACE)
            child_node.x = X_SPACE
            child_node.save()
            new_connection = Connection(a=child_node, b=node)
            new_connection.save()
            count += 1

def add_children_loc():
    for x in range(2,7):
        nodes = Node.objects.filter(level=x)
        for node in nodes:
            if node.parent.all().count() == 0:
                node.y= 250
            else:
                parent = node.parent.all()[0]
                node.y = parent.y + node.y
            node.x = (node.level - 1) * X_SPACE + 30
            node.save()

def map(request, type, id):
    nodes = Node.objects.all()
    nodes.delete()
    connections = Node.objects.all()
    connections.delete()
    new_node = Node()
    if type == "busobj":
        item = BusObj.objects.filter(id=id)[0]
        new_node.busobj = item
    elif type == "process":
        item = Process.objects.filter(id=id)[0]
        new_node.process = item
    new_node.level = item.level
    new_node.x = (item.level - 1) * X_SPACE + 30
    new_node.y = 250
    new_node.text =item.name
    new_node.description =item.description
    new_node.save()
    add_children(new_node,item.level)
    add_children_loc()
    nodes = Node.objects.all()
    connections = Connection.objects.all()
    return render(request, 'canvas.html', {'nodes': nodes, 'connections':connections})

def ind(request, type, id):
    link = ind_file[type] + ".html"
    if type == "busobj":
        item = BusObj.objects.get(pk=id)
    if type == "process":
        item = Process.objects.get(pk=id)
        processes = Process.objects.filter(parent=item)
    else:
        processes = item.process_set.all()
    return render(request, link, {'item': item, 'type': type, 'processes':processes})

def list(request,type):
    header = full_name_p[type]
    new_link = type + "_new"
    if type == "busobj":
        list = BusObj.objects.all()
    if type == "process":
        list = Process.objects.all()
    return render(request, 'list.html', {'header': header, 'type': type, 'new_link': new_link, 'list': list})

def new(request, type):
    header = "New " + full_name[type]
    if request.method == 'POST':
        if type == "busobj":
            form = BusObjForm(request.POST)
        if type == "process":
            form = ProcessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/list/' + type)
    else:
        if type == "busobj":
            form = BusObjForm()
        if type == "process":
            form = ProcessForm()
    return render(request, 'new.html', {'header': header, 'form': form})

def update(request, type, id):
    if type == "busobj":
        item = BusObj.objects.get(pk=id)
        form = BusObjForm(request.POST or None, instance=item)
    if type == "process":
        item = Process.objects.get(pk=id)
        form = ProcessForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('/list/' + type)
    header = full_name[type] + ": " + item.name
    return render(request, 'update.html', {'header': header,'item': item, 'form': form, 'type': type})

def delete(request, type, id):
    if type == "busobj":
        item = BusObj.objects.get(pk=id)
    if type == "process":
        item = Process.objects.get(pk=id)
    item.delete()
    return redirect('/list/' + type)



# TODO Show details of selected nodes
# TODO Allow multiple children
# TODO Allow multiple parents
# TODO Add a join button
# TODO Allow join selection (to edit strength or delete)
# TODO change size to fit on page
# TODO allow user to start from one node


