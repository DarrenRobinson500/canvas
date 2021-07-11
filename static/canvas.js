console.log("Found the file")

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width= window.innerWidth+250;
canvas.height = innerHeight-100;
canvas.style.background = "#bbf";
ctx.beginPath();
ctx.rect(0, 0, canvas.width, canvas.height);
ctx.stroke();
class Node{
    constructor(x,y,w,h,t,c, colour_text,highlight, highlight_b, parent) {
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.t = t;
        this.c = c;
        this.colour_text = colour_text;
        this.highlight = highlight;
        this.highlight_b = highlight_b;
        this.parent = parent;
    }
    draw(ctx){
        ctx.beginPath();
        ctx.arc(this.x,this.y,this.h/2,Math.PI/2,-Math.PI/2);
        ctx.lineTo(this.x+this.w,this.y-this.h/2);
        ctx.arc(this.x+this.w,this.y,this.h/2,-Math.PI/2,Math.PI/2);
        ctx.closePath();
        ctx.fillStyle = this.c;
        if (this.highlight) {ctx.fillStyle = "red";}
        if (this.highlight_b) {ctx.fillStyle = "red";}
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = this.colour_text;
        ctx.font = '15px arial';
        ctx.fillText(this.t,this.x,this.y+this.h*.18);
    }

    clickNode(xmouse, ymouse) {
        if (xmouse > this.x - this.h/2 && xmouse < this.x + this.w + this.h/2
         && ymouse > this.y - this.h / 2 && ymouse < this.y + this.h / 2){
            this.highlight = true;
            this.draw(ctx);
            document.getElementById("Message").innerHTML = this.t;
            return true;
        } else {
            this.highlight_b = false;
            if (this.highlight) {this.highlight = false; this.highlight_b = true;}
            this.highlight = false;
            this.draw(ctx)
            return false;
        }
    }
}

class Connection {
    constructor(child, parent, highlight) {
        this.child = child
        this.parent = parent
        this.highlight = highlight}

    draw(ctx) {
        ctx.beginPath();
        console.log(parent.x + ": " + parent.y);
        console.log(child.x + ": " + child.y);
        ctx.moveTo(this.parent.x,this.parent.y);
        ctx.lineTo(this.child.x,this.child.y);
        ctx.fill();
        ctx.closePath();
        ctx.stroke();}
}


canvas.addEventListener('click',(event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    for (let i = 0; i < nodes_js.length; i++) {
        nodes_js[i].clickNode(x,y);
    }

});

// create js nodes and connections
const nodes_js = []
{% for node in nodes %}
    var node = new Node({{node.x}},{{node.y}},100,30, "{{node.t}}", "blue", "white", false, false, )
    nodes_js.push(node);
{% endfor %}



const connections_js = []
{% for connection in connections %}
    for (let i = 0; i < nodes_js.length; i++) {
        if (nodes_js[i].t == "{{connection.a}}") {child = nodes_js[i];console.log("Child: "+nodes_js[i].t + " vs " + "{{connection.a}}");}
        if (nodes_js[i].t == "{{connection.b}}") {parent = nodes_js[i];console.log("Parent: "+nodes_js[i].t + " vs " + "{{connection.b}}");}
    }
    console.log("New connection: " + child.t+ "-"+parent.t);
    var connection = new Connection(child, parent, false);
    connections_js.push(connection);
{% endfor %}

for (let i = 0; i < connections_js.length; i++) {
    console.log("Draw connection:" + connections_js[i].child.t + connections_js[i].parent.t);
    connections_js[i].draw(ctx);
}
for (let i = 0; i < nodes_js.length; i++) {
    nodes_js[i].draw(ctx);
}


