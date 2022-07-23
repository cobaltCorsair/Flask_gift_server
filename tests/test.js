// тестовый запрос на добавление нового пользователя
$.ajax({
    url: "http://127.0.0.1:5000/addnewuser",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'name': 'Сай', 'id': 2}),
});

// тестовый запрос на удаление пользователя с неким id
$.ajax({
    url: "http://127.0.0.1:5000/deleteuser",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'forum_id': 1}),
});

// тестовый запрос на добавление нового подарка
$.ajax({
    url: "http://127.0.0.1:5000/addnewpresent",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'name': 'Подарок', 'title': 'тут какое-то описание', 'image': 'юрл картинки'}),
});

// тестовый запрос на получение подарков пользователя с неким id
$.ajax({
    url: "http://127.0.0.1:5000/getuserpresents",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'id': 1}),
});

// тестовый запрос на удаление подарка с неким id
$.ajax({
    url: "http://127.0.0.1:5000/deletepresent",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'id': 1}),
});

// тестовый запрос на удаление сделанного подарка с неким id
$.ajax({
    url: "http://127.0.0.1:5000/deletemadepresent",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'id': 1}),
});

// тестовый запрос на добавление подарков пользователю
$.ajax({
    url: "http://127.0.0.1:5000/makepresent",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({'addressee': 3, 'sender': 4, 'id_present': 2, 'comment': 'тут какое-то описание'}),
});

// тестовый запрос на вывод всех подарков, которые есть в наличии
$.ajax({
    url: "http://127.0.0.1:5000/getallpresents",
    type: "POST",
    contentType: "application/json",
});

// тестовый запрос на вывод всех пользователей в бд
$.ajax({
    url: "http://127.0.0.1:5000/getallusers",
    type: "POST",
    contentType: "application/json",
});

// тестовый запрос на запись всех пользователей в бд
(async () => {
    let req = 'https://dis.f-rpg.me/api.php?method=users.get&group_id=1,2,5,9,11&limit=500'
    let response = await fetch('https://cobaltcorsair.ru/addallusers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'url': req,
        }),
    });
    let answer = await response.json();
    let get_answer = JSON.parse(JSON.stringify(answer));
    alert(get_answer['answer']);
})();