/**
 * Обработка AJAX-подгрузки комментариев
 * @param comments_array array JSON-массив переданных комментариев
 * @param request mixed Указатель текущей страницы комментариев 
 */
function processComments(comments_array, request) {
    // Достаем текущий номер страницы комментариев 
    page_current = $('#page_current').val();
    num_pages = $('#num-pages').val();
    // Проставляем его в зависимости от указателя
    switch (request) {
		case 'first':
			page_current = 1;
			break;
			  
		case 'next':
		  	if (page_current != num_pages) page_current++
		  	break;
		  	
		case 'last':
			page_current = num_pages;
			break;
			
		case 'prev':
			if (page_current != 1) page_current--
			break;
			
		case 'flow':
			break;
		default:
			page_curr = Number(request.split('_')[1])
			if (!isNaN(Number(page_curr))) {
				if (page_curr >= 1 && page_curr <= num_pages) {
					page_current = page_curr;
					}
				else page_current = 1;
				}
			else page_current = 1;
    	}
    if (request != 'flow') {
	    // Обновляем плейсхолдер и текущий номер страницы
	    $('#page_current').val(page_current);
	    $('#comments-goto-page').val('');
	    $('#comments-goto-page').attr('placeholder', page_current + ' / ' + num_pages);
	    // Очищаем предыдущие комментарии
	    $('#comments-list').fadeOut('slow');
	    $('#comments-list').empty();
    } else if (request == 'flow') {
    	// Обновляем текущий ID скролла
    	old_val = Number($('#scroll_current').attr('value'));
    	$('#scroll_current').attr('value', old_val+1);
    }
    // Обрабатываем массив
    for (comment in comments_array) {
        // Выносим данные для удобства
        c_i = 'comment-'+comments_array[comment]['comment_id']
        c_t_d = new Date(comments_array[comment]['date'])
        c_d = c_t_d.getDate() +'.'+(c_t_d.getMonth()+1)+'.'+c_t_d.getFullYear()
        c_t = comments_array[comment]['text'];
        u_i = comments_array[comment]['author_id'];
        u_p = comments_array[comment]['author_name'];
		s_i = comments_array[comment]['story_id'];
        s_t = comments_array[comment]['story_title'];
        if (request != 'flow') {
        	// Создаем и добавляем div с ID комментария
        	$('<div>', {id: c_i}).addClass('comment-item').appendTo('#comments-list');
	        // Создаем и добавляем <p> контейнер метаинформации
	        $('<p>').addClass('comment-meta').appendTo('#'+c_i);        
	        // Ссылка на пользователя        
	        $('<a>', {href: '/accounts/'+u_i+'/', text: u_p}).addClass('comment_user').appendTo('#'+c_i+' .comment-meta');
	        // Дата
	        $('<span>').addClass('comment-date').text(c_d).appendTo('#'+c_i+' .comment-meta');
	        // Текст комментария
	        $('<p>').addClass('comment_text').html(c_t).appendTo('#'+c_i);
        } else if (request == 'flow') {
        	// Создаем и добавляем div с ID комментария
        	$('<div id="'+c_i+'" class="comment-item fresh" style="display:none;">').appendTo('#comments-list');
	        // Ссылка на пользователя, дата и линк на главу
	        $('<p class="meta"><a class="authorlink" href="/accounts/'+u_i+'/">'+u_p+'</a> '+c_d+' о <a href="/story/'+s_i+'/"><b>'+s_t+'</b></a></p>').appendTo('#'+c_i);
	        // Текст комментария
	        $('<p>').addClass('comment').html(c_t).appendTo('#'+c_i);
        }
    }
    if (request != 'flow') {
    	$('#comments-list').fadeIn();
    } else if (request == 'flow') {
    	$('.fresh').each(function(){$(this).removeClass('fresh').fadeIn('slow')});
    }
}
/**
 * Обработка AJAX-подгрузки историй
 * @param comments_array array JSON-массив переданных историй
 * @param request mixed Указатель текущей страницы историй 
 */
function processStories(stories_array, request) {
	// Обновляем текущий ID скролла
    old_val = Number($('#scroll_current').attr('value'));
   	$('#scroll_current').attr('value', old_val+1);
   	// Обрабатываем массив
   	for (story in stories_array) {
   		current_story = stories_array[story]
   		// Выносим данные для удобства
   		// ID истории
   		story_id = current_story['story_id']
   		// Название
   		story_title =current_story['story_title']
   		// Описание
   		story_summary = current_story['story_summary']
   		// Голоса
   		story_vote_up_count = current_story['story_vote_up_count']
   		story_vote_down_count = current_story['story_vote_down_count']
   		// Количество слов
   		if (current_story['story_words'] == null) {
   			story_words = 'нет'
   			} else {
   			story_words = current_story['story_words']
   		}
   		// Жанры
   		story_categories = current_story['story_categories']
   		// Персонажи
   		story_characters = current_story['story_characters']
   		// Авторы
   		story_authors = current_story['story_authors']
   		// Создаем и добавляем div с ID истории
        $('<div>').attr({'id': story_id, 'style': 'display:none;'}).addClass('story-item fresh').appendTo('#comments-list');
        // Заголовок
        $('<h3>').appendTo('#'+story_id);
        $('<a>', {href: '/story/'+story_id+'/', text: story_title}).appendTo('#'+story_id+' h3');
        // Голоса
   		$('<sup>').appendTo('#'+story_id+' h3')
   		$('<span>').addClass('upvotes').text(story_vote_up_count).appendTo('#'+story_id+' h3 sup');
   		$(document.createTextNode(' / ')).appendTo('#'+story_id+' h3 sup');
   		$('<span>').addClass('downvotes').text(story_vote_down_count).appendTo('#'+story_id+' h3 sup');
   		// Контейнер метаинформации №1
   		$('<p>').addClass('meta first-meta').appendTo('#'+story_id);
   		// Жанры
   		$('<span>').addClass('category-list').appendTo('#'+story_id+' p.first-meta');
   		for (category in story_categories) {
   			cat = story_categories[category]
   			category_id = cat['category_id']
   			category_name = cat['category_name']
   			$('<a>', {href: '/search/category/'+category_id+'/', text: category_name}).addClass('gen gen-'+category_id).appendTo('#'+story_id+' span.category-list');
   		}
   		$(document.createTextNode(story_words +' слов от ')).appendTo('#'+story_id+' p.first-meta');
   		
   		for (author in story_authors) {
   			author = Number(author)
   			auth = story_authors[author]
   			author_id = auth['author_id']
   			author_name = auth['author_name']
   			if (author == 0) {$('<a>', {href: '/accounts/'+author_id+'/', text: author_name}).addClass('authorlink').appendTo('#'+story_id+' p.first-meta');}
   			if (story_authors.length > 1 && author == 0) {$(document.createTextNode(' (в соавторстве с ')).appendTo('#'+story_id+' p.first-meta');}
   			if (story_authors.length > 1 && author > 0) {
   				$('<a>', {href: '/accounts/'+author_id+'/', text: author_name}).addClass('authorlink').appendTo('#'+story_id+' p.first-meta');
   				if (author+2 == story_authors.length) {$(document.createTextNode(' и ')).appendTo('#'+story_id+' p.first-meta');}
   				if (author+3 <= story_authors.length) {$(document.createTextNode(', ')).appendTo('#'+story_id+' p.first-meta');}
   			}
   			if (author+1 == story_authors.length && story_authors.length > 1) {$(document.createTextNode(')')).appendTo('#'+story_id+' p.first-meta');}	
   		}
   		$('<p>').text(story_summary).appendTo('#'+story_id);
   		// Контейнер метаинформации №2
   		$('<p>').addClass('meta second-meta').appendTo('#'+story_id);
   		// Персонажи
   		$('<span>').addClass('character-list').appendTo('#'+story_id+' p.second-meta');
   		for (character in story_characters) {
   			char = story_characters[character]
   			character_id = char['character_id']
   			character_name = char['character_name']
   			$('<a>', {href: '/search/character/'+character_id+'/'}).append($('<img>').attr({'src': '/static/i/characters/'+character_id+'.png', 'alt': character_name, 'title': character_name})).appendTo('#'+story_id+' span.character-list');
   		}
   	}
	$('.fresh').each(function(){$(this).removeClass('fresh').fadeIn('slow')});
}
/**
 * Обработка AJAX-подгрузки глав
 * @param comments_array array JSON-массив переданных глав
 * @param request mixed Указатель текущей страницы глав 
 */
function processChapters(chapters_array, request){
	// Обновляем текущий ID скролла
    old_val = Number($('#scroll_current').attr('value'));
   	$('#scroll_current').attr('value', old_val+1);
   	// Обрабатываем массив
   	for (chapter in chapters_array) {
   		current_chapter = chapters_array[chapter]
   		chapter_id = current_chapter['chapter_id']
   		story_id = current_chapter['story_id']
   		story_title = current_chapter['story_title']
   		author_id = current_chapter['author_id']
   		author_name = current_chapter['author_name']
   		chapter_order = current_chapter['chapter_order']
   		chapter_title = current_chapter['chapter_title']
   		date = current_chapter['date']
   		text_snippet = current_chapter['text_snippet']
   		$('<div>').attr({'id': chapter_id, 'style': 'display:none;'}).addClass('story-item fresh').appendTo('#comments-list');
   		$('<h3>').appendTo('#'+chapter_id);
   		$('<a>', {href: '/story/'+story_id+'/chapter/'+chapter_order+'/', text: chapter_title}).appendTo('#'+chapter_id+' h3');
   		$('<p>').html(text_snippet).appendTo('#'+chapter_id);
   		$('<p>').addClass('meta').appendTo('#'+chapter_id);
   		$('<a>', {href: '/story/'+story_id+'/', text: story_title}).appendTo('#'+chapter_id+' p.meta');
   		$(document.createTextNode(' от ')).appendTo('#'+chapter_id+' p.meta');
   		$('<a>', {href: '/accounts/'+author_id+'/', text: author_name}).addClass('authorlink').appendTo('#'+chapter_id+' p.meta');
   		$(document.createTextNode(', '+date)).appendTo('#'+chapter_id+' p.meta');
   	}
   	$('.fresh').each(function(){$(this).removeClass('fresh').fadeIn('slow')});
}
/**
 * Подгрузка комментариев по AJAX
 */
function getComments(request) {
	switch (request) {
		case 'first':			  
		case 'next':
		case 'last':
		case 'prev':			
			data = {type : 'paged', pointer : request, page_current : $('#page_current').val()};
			break;
		case 'flow':
			data = {type : 'flow', scroll_id : $('#scroll_current').val()};
			break;
		default:
			num_pages = $('#num-pages').val();
			if (!isNaN(Number(request))) {
				if (request >= 1 && request <= num_pages) {
					page_current = Number(request);
				} else
					page_current = 1;
			} else
				page_current = 1;
			data = {type : 'direct', page_id : page_current};
			break;
		}
	$.ajax({
		cache:		false,
		data:		{data: JSON.stringify(data)},
		dataType:   'json',
		success:	function(response) {processComments(response, request);},
		error:      getAjaxErrorHandler,
		type:       'GET',
		url:        'ajax'
		});
}

/**
 * Обработчик ошибок AJAX-подгрузки
 * @param XMLHttpRequest object Объект XMLHttpRequest
 * @param ajaxOptions string Строка, описывающая тип случившейся ошибки
 * @param thrownError object Объект исключений
 */
function getAjaxErrorHandler(XMLHttpRequest, ajaxOptions, thrownError) {
    console.warn(XMLHttpRequest);
    console.warn(ajaxOptions);
    console.warn(thrownError);
}

/**
 * Подгрузка историй по AJAX
 */
function getStories(request) {
	switch (request) {
		case 'flow':
			data = {type : 'flow', scroll_id : $('#scroll_current').val()};
			break;
		}
	$.ajax({
		cache:		false,
		data:		{data: JSON.stringify(data)},
		dataType:   'json',
		success:	function(response) {processStories(response, request);},
		error:      getAjaxErrorHandler,
		type:       'GET',
		url:        'ajax'
		});
}

/**
 * Подгрузка глав по AJAX
 */
function getChapters(request) {
	switch (request) {
		case 'flow':
			data = {type : 'flow', scroll_id : $('#scroll_current').val()};
			break;
		}
	$.ajax({
		cache:		false,
		data:		{data: JSON.stringify(data)},
		dataType:   'json',
		success:	function(response) {processChapters(response, request);},
		error:      getAjaxErrorHandler,
		type:       'GET',
		url:        'ajax'
		});
}
// Функция проверки CRSF-безопасности
function csrfSafeMethod(method) { return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}

/**
 * Голосование за рассказ по AJAX
 */
requestRunning = false;
function voteStory(request) {
	if (requestRunning) { // don't do anything if an AJAX request is pending
	        return;
	}
	requestRunning = true;
	// Читаем CSRF Cookie
	var csrftoken = $.cookie('csrftoken');
	// Конфигурируем заголовок AJAX-запроса
	$.ajaxSetup({
		crossDomain: false,
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	$.ajax({
		cache:		false,
		data:		{vote: request},
		dataType:   'json',
		error:      getAjaxErrorHandler,
		success:	changeVote,
		complete:	function() {requestRunning = false;},
		type:       'POST',
		url:        'vote'
		});
}
// Обработка смены количества голосов
function changeVote(response){
	$('#vote-up').text(response[0]);
	$('#vote-down').text(response[1]);
	$('#vote-msg').html('<span class="alert alert-success">Ваш голос учтен!</span>');
	$('#vote-msg span').animate({ opacity: 0.1}, 3500, function() {$('#vote-msg span').remove();});
}
/**
 * Добавление-удаление из избранного по AJAX
 */
function favoriteStory() {
	// Читаем CSRF Cookie
	var csrftoken = $.cookie('csrftoken');
	// Конфигурируем заголовок AJAX-запроса
	$.ajaxSetup({
		crossDomain: false,
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
	$.ajax({
		cache:		false,
		error:      getAjaxErrorHandler,
		success:	changeFavorite,
		type:       'POST',
		url:        'favorite'
		});
}
// Обработка добавления-удаления из избранного
function changeFavorite(response){
	$('#favstar').toggleClass('faved');
	if (response == '0') {
	var text = 'Рассказ удален из избранного';
	} else if (response == '1') {
	var text = 'Рассказ добавлен в избранное';
	}
	$('#fav-msg').append('<span class="alert alert-success">'+text+'</span>')
	$('#fav-msg span').animate({ opacity: 0.1}, 3500, function() {$('#fav-msg span').remove();});
}

// При загрузке страницы
$(function(){
	//Включаем карусель
	$('#myCarousel').slides({
		generatePagination: false,
		play: 5000,
		pause: 2500,
		hoverPause: true,
		});
    // Включаем обработку BootStrap Buttons
    // TODO: Всерьёз заняться оптимизированием кода!
	$('.bootstrap').each(function(){
		var group = $(this);
		var buttons_container = $('.buttons-visible', group)
		var data_container = $('.buttons-data', group)
		
		if (group.hasClass('checkboxes')) {
			var type = 'checkboxes'
		} else if (group.hasClass('radio')) {
			var type = 'radio'
		}
		// Обработка проставленных заранее чекбоксов и радиоселектов
		$('input', data_container).each(function() {
			var input = $(this);
			value = input.attr('value')
			checked = Boolean(input.attr('checked'))
			if (checked) {
				buttons_container.children('button[value='+value+']').addClass('active');
			}			
		});
		// Onclick-обработчик
		$('button', buttons_container).each(function() {
			var button = $(this);
			button.live('click', function() {
				value = button.attr('value');
				if (type == 'checkboxes') {	
				    input = $('input:checkbox[value='+value+']', data_container);
                    selected = Boolean($('input:checked[value='+value+']', data_container).length);
                    selected ? input.removeAttr('checked') : input.attr('checked','checked');
	            } else if (type == 'radio'){
	                input = $('input:radio[value='+value+']', data_container);
	            	all_inputs = $('input:radio', data_container);
	            	all_inputs.removeAttr('checked');
	            	input.attr('checked','checked');
	            }
			});
		});
    });
    // Подключаем обработку выбора персонажей
	$(".character-item").click(function() {          
	    if(Boolean($(this).children('input:checked').length)) {
	    	$(this).children('img').removeClass('ui-selected');
	    	$(this).children('input').removeAttr('checked');
	    	}
	    else {
	    	$(this).children('img').addClass("ui-selected");
	    	$(this).children('input').attr('checked','checked');
	    	}
	});
	// Очистка формы поиска 
	$("#reset_search").click(function() {          
		$('input:checked').removeAttr('checked');
		$('button').removeClass('active');
		$('img').removeClass('ui-selected');
		document.getElementById('appendedInputButtons').setAttribute('value','');
		$('.span8').slideUp();
	});
	// Подгрузка комментариев по прокрутке
	$(window).scroll(function() {
		if (window.location.pathname == "/stream/comments/" && ($('.container').height()+20 == $(window).height()+$(this).scrollTop())){
        	$('.loader').fadeIn('fast');
            getComments('flow');
            $('.loader').fadeOut('fast');
        }
    });
	// Подгрузка историй по прокрутке
	$(window).scroll(function() {
		if (window.location.pathname == "/stream/stories/" && ($('.container').height()+20 == $(window).height()+$(this).scrollTop())){
        	$('.loader').fadeIn('fast');
            getStories('flow');
            $('.loader').fadeOut('fast');
        }
    });
    // Подгрузка глав по прокрутке
	$(window).scroll(function() {
		if (window.location.pathname == "/stream/chapters/" && ($('.container').height()+20 == $(window).height()+$(this).scrollTop())){
        	$('.loader').fadeIn('fast');
            getChapters('flow');
            $('.loader').fadeOut('fast');
        }
    });
    // На странице поиска...
    var re_search = new RegExp('/search/(.+)?');
    if (re_search.test(window.location.pathname)){
    	// ...проставляем классы изображениям персонажей, в зависимости от выбранных скрытых чекбоксов.
		$('input[name="characters_select"][checked="checked"]').parent().children('img').addClass('ui-selected');
    }
    // На странице редактирования истории...
    var re_storyedit = new RegExp('/story/[0-9]+/edit/')
    if (re_storyedit.test(window.location.pathname)){
    	// ...проставляем классы изображениям персонажей, в зависимости от выбранных скрытых чекбоксов.
		$('.character-item input[checked="checked"]').prev().addClass('ui-selected');
		// ...подключаем возможность сортировки глав "на лету"
		$('#sortable_chapters').sortable({
			// Действия при обновлении
			update: function(){
				// Читаем CSRF Cookie
				var csrftoken = $.cookie('csrftoken');
				// Конфигурируем заголовок AJAX-запроса
				$.ajaxSetup({
					crossDomain: false,
					beforeSend: function(xhr, settings) {
						if (!csrfSafeMethod(settings.type)) {
							xhr.setRequestHeader("X-CSRFToken", csrftoken);
						}
    				}
				});
				// Посылаем AJAX-запрос
				$.ajax({
					cache:		false,
					data:		$('#sortable_chapters').sortable('serialize'),
					error:      getAjaxErrorHandler,
					type:       'POST',
					url:        'ajax'
				});
			}
		});
    }
    // На странице добавления или редактирования главы
    var re_chapteredit = new RegExp('/story/[0-9]+/chapter/[0-9]+/edit/')
    var re_chapteradd = new RegExp('/story/[0-9]+/chapter/add/')
    if (re_chapteredit.test(window.location.pathname) || re_chapteradd.test(window.location.pathname)){
    $('.chapter-textarea').markItUp(mySettings);
		$('#id_notes').markItUp(mySettings);
    }
    // Голосование
	$('#vote-up').click(function() {
    	voteStory('1');
    });
	$('#vote-down').click(function() {
    	voteStory('-1');
    });
	$('#favstar').click(function(){favoriteStory()});
	// Переключение размера и типа шрифта
	$('.select-font').change(function() {
	    if($('.select-font').val() == '1')
	    $('.chapter-text').removeClass('mono-font serif-font')
	    else if($('.select-font').val() == '2')
	    $('.chapter-text').removeClass('mono-font').addClass('serif-font')
	    else if($('.select-font').val() == '3')
	    $('.chapter-text').removeClass('serif-font').addClass('mono-font')
	});
	$('.select-size').change(function() {
	    if($('.select-size').val() == '1')
	    $('.chapter-text').removeClass('small-font big-font')
	    else if($('.select-size').val() == '2')
	    $('.chapter-text').removeClass('big-font').addClass('small-font')
	    else if($('.select-size').val() == '3')
	    $('.chapter-text').removeClass('small-font').addClass('big-font')
	});
	// Ещё какая-то ерунда
	// ---
});