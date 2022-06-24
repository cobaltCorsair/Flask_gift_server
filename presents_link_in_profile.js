// добавляем ссылку на страницу с подарками в профиль в постах
    function add_link() {
            $("#pun-viewtopic .post .post-author").each(function() {
                    let added_id = $(this).closest('.post').attr('data-user-id');
                    let presents_personal_link = '<strong><a href=\"/pages/random_user_page?id=' +added_id+ '\"' + 'title=\"тест\" target=\"_blank\">Подарки</a></strong>';
                    $(this).find('.pa-fld3').html(presents_personal_link);

            });
            let profile_id = $('#viewprofile-next').attr('class').split(' ')[1].replace('id-', '');
            let profile_personal_link = '<a href=\"/pages/random_user_page?id=' +profile_id+ '\"' + 'title=\"тест\" target=\"_blank\">страница</a>';
            $('#pa-fld3').find('strong').html(profile_personal_link);
    }
    add_link();