function toggle(source) {
    const checkboxes =  document.getElementsByClassName('checkall')
    for (var i = 0; i< checkboxes.length; i++){
        checkboxes[i].checked = source.checked
    }
}

var url = 'http://127.0.0.1:8000/api/users/'
const csrf = document.getElementsByName('csrfmiddlewaretoken')

function builtTable(){
    var table_body = document.getElementById('table_body')
    table_body.innerHTML = ''

    fetch(url)
    .then((resp) => resp.json())
    .then(function(data){
        console.log(data)
        var list = data
        for (var i in list){
            var item = `
                <tr>
                    <td><input type="checkbox" class="checkall" id="checks" name="checks[]" value="${list[i].id}"></td>
                    <td>${list[i].id}</td>
                    <td>${list[i].user.username}</td>
                    <td>${list[i].user.email}</td>
                    <td>${list[i].user.date_joined}</td>
                    <td>${list[i].user.last_login}</td>
                    <td>${list[i].status}</td>
                </tr>
            `
            table_body.innerHTML += item
        }
    })

}

builtTable()

const delete_button = $(".delete_button")[0]
const block_button = $(".block_button")[0]
const unblock_button = $(".unblock_button")[0]

delete_button.addEventListener('click', function(e){
    e.preventDefault()
    console.log('from deleete')
    const checkboxes =  document.getElementsByClassName('checkall')
    console.log(checkboxes)
    for (var i = 0; i< checkboxes.length; i++){
        if(checkboxes[i].checked == true){
            var delete_url = `http://127.0.0.1:8000/users/delete/${checkboxes[i].value}/`
            $.ajax({
                type: 'DELETE',
                url: delete_url,
                dataType: "json",
                headers: {
                    'Content-type': 'application/json',
                    'X-CSRFToken': csrf[0].value,
                },
                success: function (response) {
                    console.log(response)

                },
                error: function (response) {
                    console.log(response)
                }
    })
        }
    }
    window.location.href = 'http://127.0.0.1:8000/'

})

block_button.addEventListener('click', function(e){
    e.preventDefault()
    const checkboxes =  document.getElementsByClassName('checkall')
    console.log(checkboxes)
    for (var i = 0; i< checkboxes.length; i++){
        if(checkboxes[i].checked == true){
            var ban_url = `http://127.0.0.1:8000/api/users/${checkboxes[i].value}/`
            var data = {"status": "Banned"}
            $.ajax({
                type: 'PATCH',
                data: JSON.stringify(data),
                url: ban_url,
                dataType: "json",
                headers: {
                    'Content-type': 'application/json',
                    'X-CSRFToken': csrf[0].value,
                },
                success: function (response) {
                    console.log(response)

                },
                error: function (response) {
                    console.log(response)
                }
    })
    }
        }
        window.location.href = 'http://127.0.0.1:8000/'

    })


unblock_button.addEventListener('click', function(e){
    e.preventDefault()
    const checkboxes =  document.getElementsByClassName('checkall')
    console.log(checkboxes)
    for (var i = 0; i< checkboxes.length; i++){
        if(checkboxes[i].checked == true){
            var ban_url = `http://127.0.0.1:8000/api/users/${checkboxes[i].value}/`
            var data = {"status": "Unbanned"}
            $.ajax({
                type: 'PATCH',
                data: JSON.stringify(data),
                url: ban_url,
                dataType: "json",
                headers: {
                    'Content-type': 'application/json',
                    'X-CSRFToken': csrf[0].value,
                },
                success: function (response) {
                    console.log(response)

                },
                error: function (response) {
                    console.log(response)
                }
    })
    }
        }
        window.location.href = 'http://127.0.0.1:8000'

    })