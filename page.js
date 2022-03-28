<div class="Basket"></div>

<script type="text/javascript">

    (async () => {
    let response = await fetch('http://127.0.0.1:5000/getallpresents', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json'
}
});
    let result = await response.json();
    let data = JSON.parse(JSON.stringify(result));
    let out = '';
    for(let key in data) {
    out+='<div class="item" data-id="'+data[key]['id']+'"';
    out+=' data-name="' +data[key]['name']+'"';
    out+=' data-desc="'+data[key]['title']+'">';
    out+='<div class="item_image"><div class="item_container"><img src="'+data[key]['image']+'" width="41" height="40"></div></div>';
    out+='<template id="'+data[key]['id']+'">';
    out+='<div class="item-desc">'+data[key]['title']+'</div></template></div>';
};

    $('.Basket').html(out);
})();

</script>