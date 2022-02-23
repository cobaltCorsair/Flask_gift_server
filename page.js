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
    out+='<div id="present"><h3>'+data[key]['id']+'</h3>';
    out+='<p>'+data[key]['name']+'</p>';
    out+='<p>'+data[key]['title']+'</p>';
    out+='<img src="'+data[key]['image']+'"></div>'; // Формируем URL картинки
};

$('.Basket').html(out);
})();
</script>