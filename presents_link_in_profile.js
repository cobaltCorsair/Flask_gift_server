// добавляем ссылку на страницу с подарками в профиль в постах
let random_user_page_name = 'random_user_page'; // название страницы рандомного юзера в админке
let profile_field_id = 'fld3' // id поля профиля, где находится ссылка на страницу подарков

    function add_link() {
            $("#pun-viewtopic .post .post-author").each(function() {
                    let added_id = $(this).closest('.post').attr('data-user-id');
                    let presents_personal_link = '<strong id="presentsPage"><a href=\"/pages/'+ random_user_page_name + '?id=' +added_id+ '\"' + 'title=\"Страница подарков\" target=\"_blank\">Подарки</a></strong>';
                    $(this).find('.pa-'+profile_field_id).html(presents_personal_link);

            });
            let profile_id = $('#viewprofile-next').attr('class').split(' ')[1].replace('id-', '');
            let profile_personal_link = '<a href=\"/pages/'+ random_user_page_name +'?id=' +profile_id+ '\"' + 'title=\"Страница подарков\" target=\"_blank\">Подарки</a>';
            $('#pa-'+profile_field_id).find('strong').html(profile_personal_link);
    }
    add_link();