$.ajax({
    url: "http://127.0.0.1:5000/addnewuser",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'name':'test', 'id':8}),
});

$.ajax({
    url: "http://127.0.0.1:5000/addnewpresent",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'name':'Подарок', 'title':'тут какое-то описание', 'image': 'юрл картинки'}),
});

$.ajax({
    url: "http://127.0.0.1:5000/getuserpresents",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'id': 1}),
});

$.ajax({
    url: "http://127.0.0.1:5000/makepresent",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'addressee': 3, 'sender': 4,
        'id_present': 2, 'present_name': 'Подарок1', 'comment': 'тут какое-то описание'}),
});