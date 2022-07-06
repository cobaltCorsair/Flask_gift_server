// добавляем ссылку на страницу с подарками в профиль в постах
const USER_PAGE = 'user_page'; // адрес страницы юзера в админке
const GIFTS_PAGE = 'gifts_page'; // адрес страницы магазина подарков в админке
const PROFILE_FIELD_ID = 'fld1'; // id поля профиля, где находится ссылка на страницу подарков
const GROUPS_FOR_LIST = [1, 2, 5, 9, 11]; // группы, которым можно дарить подарки
// чтобы ссылка начала отображаться, в поле должно быть хоть что-нибудь написано

function add_link() {
    if (GROUPS_FOR_LIST.indexOf(GroupID) !== -1) {
        // ссылка в главном меню форума на свою страницу
        let my_page_url = '<li id="myPage"><a href=\"/pages/' + USER_PAGE + '?id=' + UserID + '\"' + 'title=\"Страница подарков\" target=\"_blank\">Мои подарки</a></li>';
        // ссылка на магазин
        let gifts_shop_link = '<li id="shopPage"><a href=\"/pages/' + GIFTS_PAGE + '\"' + 'title=\"Галерея подарков\" target=\"_blank\">Галерея подарков</a></li>';
        $("#navprofile").after(my_page_url);
        $("#navpm").after(gifts_shop_link);
    }
    // ссылка в постах
    $("#pun-viewtopic .post .post-author").each(function () {
        let added_id = $(this).closest('.post').attr('data-user-id');
        let presents_personal_link = '<strong id="presentsPage"><a href=\"/pages/' + USER_PAGE + '?id=' + added_id + '\"' + 'title=\"Страница подарков\" target=\"_blank\">Подарки</a></strong>';
        $(this).find('.pa-' + PROFILE_FIELD_ID).html(presents_personal_link);

    });
    // ссылка при просмотре профиля
    if ($('#viewprofile-next').length > 0) {
        let profile_id = $('#viewprofile-next').attr('class').split(' ')[1].replace('id-', '');
        let profile_personal_link = '<a href=\"/pages/' + USER_PAGE + '?id=' + profile_id + '\"' + 'title=\"Страница подарков\" target=\"_blank\">Подарки</a>';
        $('#pa-' + PROFILE_FIELD_ID).find('strong').html(profile_personal_link);
    }
}

add_link();