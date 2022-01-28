$.ajax({
    url: "http://127.0.0.1:5000/getandpost",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'Name':'test', 'id':8}),
});