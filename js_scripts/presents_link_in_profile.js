// добавляем ссылку на страницу с подарками в профиль в постах и в просмотре
const SERVER_PATH = 'https://cobaltcorsair.ru/'; // адрес сервера
const USER_PAGE = 'user_page'; // адрес страницы юзера в админке
const PROFILE_FIELD_ID = 'fld4'; // id поля профиля, где находится ссылка на страницу подарков
// чтобы ссылка начала отображаться, в поле должно быть хоть что-нибудь написано

function add_link(data) {
    // ссылка в постах
    if ($('#pun-viewtopic .post .post-author').length > 0) {
        $("#pun-viewtopic .post .post-author").each(function() {
            let added_id = $(this).closest('.post').attr('data-user-id');
            let presents_personal_link = '<strong id="presentsPage"><a href=\"/pages/' + USER_PAGE + '?id=' + added_id + '\"' + 'title=\"Страница подарков\" target=\"_blank\">Подарки: </a></strong>';
            if (typeof data[added_id] !== "undefined") {
                presents_personal_link += data[added_id];
            } else {
                presents_personal_link += '0';
            }
            $(this).find('.pa-' + PROFILE_FIELD_ID).html(presents_personal_link);
        });
    }

    // ссылка при просмотре профиля
    if ($('#viewprofile-next').length > 0) {
        let profile_id = $('#viewprofile-next').attr('class').split(' ')[1].replace('id-', '');
        let profile_personal_link = '<a href=\"/pages/' + USER_PAGE + '?id=' + profile_id + '\"' + 'title=\"Страница подарков\" target=\"_blank\">Подарки: </a>';
        if (typeof data[profile_id] !== "undefined") {
            profile_personal_link += data[profile_id];
        } else {
            profile_personal_link += '0';
        }
        $('#pa-' + PROFILE_FIELD_ID).find('strong').html(profile_personal_link);
    }
}
// получаем количество подарков у пользователей
function getStatistic() {
    return (async () => {
        let response = await fetch(SERVER_PATH + 'getpresentscount', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        let result = await response.json();
        let data = JSON.parse(JSON.stringify(result));
        return data['answer'];
    })();
}
getStatistic().then(res => {
        let data = res;
        add_link(data);
    })
    .catch(err => {
        console.log(err);
    });