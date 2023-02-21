"use strict";

const cells = [["00", "01" , "02"], ["10", "11", "12"], ["20", "21", "22"]];
let matrix = [[...cells[0]], [...cells[1]], [...cells[2]]];
const WINNING_COLOR = "green";
let turn = "img/o.png"; 
//let turn = "img/x.png";
let moves = 0;
let height;

function setHeight()
{
    for (let i=0; i<cells.length; i++)
    {
        cells[i].forEach(function(element, index, array){

            let item = document.getElementById(element);
            height = item.offsetWidth;
            item.style.height = height+'px';
            array[index] = true;

        });
    }

    let body = document.getElementById("body");
    body.addEventListener('keydown', (event)=>{

        let select = document.getElementById("select");

        if (event.key === "Control")
            select.style.visibility = "visible";

        if (event.key === "x")
            select.style.visibility === "hidden";
    });
}

function check(id)
{
    let i = parseInt(id[0]);
    let j = parseInt(id[1]);

    if (cells[i][j])
    {
        let cell = document.getElementById(id);
        let svg = document.createElement("img");
        let path = change();
        svg.setAttribute("height", height+'px');
        svg.setAttribute("weight", height+'px');
        svg.setAttribute("src", path);
        svg.setAttribute("name", path);
        cell.appendChild(svg)
        cells[i][j] = false;
        moves++;
    
        if (moves > 4)
            calculate();
    }
}

function uncheck(id)
{
    let i = parseInt(id[0]);
    let j = parseInt(id[1]);

    if (!cells[i][j])
    {
        let cell = document.getElementById(id);
        cell.removeChild(cell.firstChild);
        cells[i][j] = true;
        change();
        moves--;
    }
}

function over(id)
{
    let cell = document.getElementById(id);
    let color = cell.style.backgroundColor;
    let img = cell.firstChild;

    if (img !== null && color !== WINNING_COLOR)
    {
        cell.style.backgroundColor = "red";
        return;
    }

    if (color === WINNING_COLOR)
        return;

    cell.style.backgroundColor = "yellow";
}

function out(id)
{
    let cell = document.getElementById(id);
    let color = cell.style.backgroundColor;

    if (color === WINNING_COLOR)
        return;

    cell.style.backgroundColor = "white";
}

function change()
{
    if (turn === "img/o.png")
    {
        turn = "img/x.png";
        return "img/o.png";
    }
    else
    {
        turn = "img/o.png";
        return "img/x.png";
    }
}

function calculate()
{
    for (let i=0; i<matrix.length; i++)
        if (consecutive(...matrix[i]))
            return;

    let t = transpose(matrix);

    for (let i=0; i<t.length; i++)
        if (consecutive(...t[i]))
            return;

    if (consecutive("00", "11", "22"))
        return;
    else
        consecutive("02", "11", "20");
}

function consecutive(one, two, three)
{
    one = document.getElementById(one).firstChild;
    two = document.getElementById(two).firstChild;
    three = document.getElementById(three).firstChild;

    if (!nulls(one, two, three) && names(one, two, three))
    {
        win(one, two, three);
        return true;
    }
    else 
        return false;
}

function nulls(one, two, three)
{
    return one===null || two===null || three===null;
}

function names(one, two, three)
{
    return one.getAttribute("name") === two.getAttribute("name") && two.getAttribute("name") === three.getAttribute("name");
}

function win(one, two, three)
{
    one.parentElement.style.backgroundColor = WINNING_COLOR;
    two.parentElement.style.backgroundColor = WINNING_COLOR;
    three.parentElement.style.backgroundColor = WINNING_COLOR;
}

function transpose(ndim)
{
    let result = [[]];

    let row_1 = ndim[0];
    let row_2 = ndim[1];
    let row_3 = ndim[2];

    for (let i=0; i<ndim.length; i++)
        result[i] = [row_1[i], row_2[i], row_3[i]];

    return result;
}

function select()
{
    turn = document.getElementById("select").value;
}