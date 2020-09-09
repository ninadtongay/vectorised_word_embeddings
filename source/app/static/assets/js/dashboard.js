$(document).on('keyup', '#set-rows1', function(){
    if(document.getElementById('set-rows1').value > 0){
        $('.set-rows2').attr('hidden', false);
    } else {
        $('.set-rows2').attr('hidden', true);
    }
});

$(document).on('keyup', '#set-rows2', function(){
    if(document.getElementById('set-rows2').value > 0){
        $('.city-post-select').attr('hidden', false);
    } else {
        $('.city-post-select').attr('hidden', true);
    }
});

$('#city-post-select').on('change', function(){
    if($('#city-post-select').val()  == "City"){
        $('.city-select').attr('hidden', false);
        $('.post-select').attr('hidden', true);
    } else {
        $('.post-select').attr('hidden', false);
        $('.city-select').attr('hidden', true);
    }
});

$('.option-select').on('change', function(){
    $('.set-threshold').attr('hidden', false);
    console.log($('#city-post-select').val());
    if($('#city-post-select').val() == "City"){
        $('.expected-output-city').attr('hidden', false);
        $('.expected-output-post').attr('hidden', true);
    } else {
        $('.expected-output-post').attr('hidden', false);
        $('.expected-output-city').attr('hidden', true);
    }
});

$(document).ready(function(){

    $.ajax({
        url: "/get_all_items",
        method: 'GET',
        success: function(result){
            $('.items-list-result > #result-row').remove()
            $('.items-list-headers > #result-headers').remove()
            var keys = [];
            for(var k in result[0]) keys.push(k);
            for(var k in result[0]) $('.items-list-headers').append("<th id='result-headers'>" + k + "</th>");
            for(i=0;i<result.length;i++){
                $('.items-list-result').append("<tr id = 'result-row' class='result-row-" + i + "'></tr>");
                for(j=0;j<keys.length;j++){
                    $('.result-row-' + i).append("<td>" + result[i][keys[j]] + "</td>");
                }
                $('.result-row-' + i).append("<td><span class='selectgroup-button btn-danger' style='color:white;' id='delete-item' data-id='" + result[i][keys[0]] + "'><i class='fa fa-times'></i></span></td>");
            }
        }
    });

});

$('.admin-operation#execute-button').on('click', function(){

    $('#model-time').text('');
    $('#original-time').text('');
    $('#time-difference').text('');
    $('#accuracy').text('');
    $('#f1_score').text('');

    n1 = document.getElementById('set-rows1').value;
    n2 = document.getElementById('set-rows2').value;
    choice = document.getElementById('city-post-select').value;
    city = document.getElementById('city-select').value;
    post = document.getElementById('post-select').value;
    thresh = document.getElementById('set-threshold').value;
    expected_output_city = $('#expected-output-city').val();
    expected_output_post = $('#expected-output-post').val();
    $.ajax({
        url: "/execute",
        method: 'GET',
        traditional: true,
        data: {
            'n1': n1,
            'n2': n2,
            'choice': choice,
            'city': city,
            'post': post,
            'thresh': thresh,
            'expected_output_city': expected_output_city,
            'expected_output_post': expected_output_post,
        },
        success: function(result){
            $('#model-time').text(result['model_execution_time']);
            $('#original-time').text(result['regular_execution_time']);
            $('#time-difference').text(result['time-difference']);
            $('#accuracy').text(result['accuracy']);
            $('#f1_score').text(result['f1_score']);
            // $('.items-list-result > #result-row').remove()
            // $('.items-list-headers > #result-headers').remove()
            // var keys = [];
            // for(var k in result[0]) keys.push(k);
            // for(var k in result[0]) $('.items-list-headers').append("<th id='result-headers'>" + k + "</th>");
            // for(i=0;i<result.length;i++){
            //     $('.items-list-result').append("<tr id = 'result-row' class='result-row-" + i + "'></tr>");
            //     for(j=0;j<keys.length;j++){
            //         $('.result-row-' + i).append("<td>" + result[i][keys[j]] + "</td>");
            //     }
            //     $('.result-row-' + i).append("<td><span class='selectgroup-button btn-danger' style='color:white;' id='delete-item' data-id='" + result[i][keys[0]] + "'><i class='fa fa-times'></i></span></td>");
            // }
        }
    });
});