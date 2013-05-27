requestRunning = false;

/**
 * ОБРАБОТЧИКИ
 */

var ajax = {

    /**
     * Обработчик ошибок AJAX-подгрузки
     * 
     * @param XMLHttpRequest
     *                object Объект XMLHttpRequest
     * @param ajaxOptions
     *                string Строка, описывающая тип случившейся ошибки
     * @param thrownError
     *                object Объект исключений
     */
    errorhandler : function(XMLHttpRequest, ajaxOptions, thrownError) {
	console.warn(XMLHttpRequest);
	console.warn(ajaxOptions);
	console.warn(thrownError);
    },
    /**
     * Отображение модального окна
     * 
     * @param event
     *                event Событие
     */
    modal : function(event) {
	event.stopImmediatePropagation();
	event.preventDefault();
	$('.modal:hidden').remove(); // Fix fox clear DOM
	var url = '/ajax' + $(this).attr('href');
	var modal = $('<div class="modal hide fade"></div>');
	$.get(url, function(data) {
	    modal.html(data).on('show', function() {
		var textarea = $('textarea', this);
		if (textarea.length) {
		    textarea.markItUp(mySettings);
		}
	    }).modal();
	});
    },
    /**
     * Работа с комментариями
     */
    comment : {
	/**
	 * Подгрузка комментариев
	 * 
	 * @param url
	 *                string Адрес страницы подгрузки
	 */
	load : function(url) {
	    var re_page = new RegExp('/comments/page/([0-9]+)/$');
	    var go_page = url.match(re_page)[1] | 0;
	    $.ajax({
		type : 'GET',
		dataType : 'html',
		success : function(response) {
		    ajax.comment.process(response, go_page);
		},
		url : url
	    });
	},
	/**
	 * Обработка подгрузки комментариев
	 * 
	 * @param comments
	 *                string HTML-код переданных комментариев
	 * @param page_current
	 *                int Текущая страница комментариев
	 */
	process : function(comments, page_current) {
	    var num_pages = $('#num_pages').val();
	    var prev_link = $('#ajax_prev_comment');
	    var next_link = $('#ajax_next_comment');
	    var re_link = new RegExp('(.+)comments/page/[0-9]+/$');
	    var new_href_prev_link = prev_link.attr('href').match(re_link)[1] + 'comments/page/' + (page_current - 1) + '/';
	    var new_href_next_link = next_link.attr('href').match(re_link)[1] + 'comments/page/' + (page_current + 1) + '/';
	    prev_link.attr('href', new_href_prev_link);
	    next_link.attr('href', new_href_next_link);
	    $('#comments-list').fadeOut('slow').empty().append(comments).fadeIn();
	    $('#ajax_pages_comment').text(page_current + '/' + num_pages);
	    if (page_current == 1) {
		prev_link.addClass('hidden');
		next_link.removeClass('hidden');
	    } else if (page_current == num_pages) {
		next_link.addClass('hidden');
		prev_link.removeClass('hidden');
	    } else {
		next_link.removeClass('hidden');
		prev_link.removeClass('hidden');
	    }
	},
	/**
	 * Удаление комментария
	 * 
	 * @param event
	 *                event Событие
	 */
	remove : function(event) {
	    event.stopImmediatePropagation();
	    event.preventDefault();
	    var url = '/ajax' + $(this).attr('href');
	    $.post(url, function(data) {
		$('#comment_' + data).slideUp('slow').remove();
	    }).success(function() {
		$('.modal').modal('hide').remove();
	    });
	},
	/**
	 * Отправка комментария
	 * 
	 * @param event
	 *                event Событие
	 */
	send : function(event) {
	    event.stopImmediatePropagation();
	    event.preventDefault();
	    form = $('.modal form');
	    var url = '/ajax' + form.attr('action');
	    $.ajax({
		type : "POST",
		url : url,
		data : form.serialize(),
		success : function(data) {
		    var new_comment = $(data);
		    var new_text = $('div.comment', new_comment);
		    var target = $('#' + new_comment.attr('id') + ' div.comment');
		    if (target.length) {
			target.replaceWith(new_text);
		    } else {
			$('#comments-list').prepend(new_comment);
		    }
		    $('.modal').modal('hide').remove();
		}
	    });
	},

    },
    /**
     * Работа с рассказами
     */
    story : {
	/**
	 * Публикация рассказа
	 * 
	 * @param response
	 *                int ID рассказа
	 */
	publish : function(response) {
	    if (pages.story_view.regex.test(window.location.pathname)) {
		var btn = $('.story_publish');
	    } else {
		var btn = $('#story_' + response + ' .story_publish');
	    }
	    if (btn.hasClass('btn-primary')) {
		var text = 'В черновики';
	    } else {
		var text = 'Опубликовать';
	    }
	    btn.text(text).toggleClass('btn-primary');
	},
	/**
	 * Одобрение рассказа
	 * 
	 * @param response
	 *                int ID рассказа
	 */
	approve : function(response) {
	    if (pages.story_view.regex.test(window.location.pathname)) {
		var btn = $('.story_approve');
	    } else {
		var btn = $('#story_' + response + ' .story_approve');
	    }
	    if (btn.hasClass('btn-success')) {
		var text = 'Отменить';
	    } else {
		var text = 'Одобрить';
	    }
	    btn.text(text).toggleClass('btn-success');
	},

	/**
	 * Обработать закладку рассказа
	 * 
	 * @param response
	 *                int ID рассказа
	 */
	bookmark : function(response) {
	    if (pages.story_view.regex.test(window.location.pathname)) {
		var btn = $('.story_bookmark');
		var msg_container = $('.story_bookmark ~ .story_bookmark_msg');
	    } else {
		var btn = $('#story_' + response + ' .story_bookmark');
		var msg_container = $('#story_' + response + ' .story_bookmark ~ .story_bookmark_msg');
	    }
	    if (btn.hasClass('bookmarked')) {
		var text = 'Рассказ удален из закладок';
	    } else {
		var text = 'Рассказ добавлен в закладки';
	    }
	    btn.toggleClass('bookmarked');
	    msg_container.append('<span class="alert alert-warning alert-mini">' + text + '</span>');
	    msg_container.children().animate({
		opacity : 0.01
	    }, 3000, function() {
		msg_container.children().remove();
	    });
	},

	/**
	 * Обработать избранность рассказа
	 * 
	 * @param response
	 *                int ID рассказа
	 */
	favorite : function(response) {
	    if (pages.story_view.regex.test(window.location.pathname)) {
		var btn = $('.story_favorite');
		var msg_container = $('.story_favorite ~ .story_favorite_msg');
	    } else {
		var btn = $('#story_' + response + ' .story_favorite');
		var msg_container = $('#story_' + response + ' .story_favorite ~ .story_favorite_msg');
	    }
	    if (btn.hasClass('favorited')) {
		var text = 'Рассказ удален из избранного';
	    } else {
		var text = 'Рассказ добавлен в избранное';
	    }
	    btn.toggleClass('favorited');
	    msg_container.append('<span class="alert alert-warning alert-mini">' + text + '</span>');
	    msg_container.children().animate({
		opacity : 0.01
	    }, 3000, function() {
		msg_container.children().remove();
	    });
	},
	/**
	 * Голосование за рассказ
	 * 
	 * @param url
	 *                string Адрес
	 */
	vote : function(url) {
	    if (requestRunning) {
		return;
	    }
	    requestRunning = true;
	    $.ajax({
		dataType : 'json',
		success : function(response) {
		    $('#vote-up').text(response[0]);
		    $('#vote-down').text(response[1]);
		    $('#vote-msg').html('<span class="alert alert-success">Ваш голос учтен!</span>');
		    $('#vote-msg span').animate({
			opacity : 0.1
		    }, 3500, function() {
			$('#vote-msg span').remove();
		    });
		},
		complete : function() {
		    requestRunning = false;
		},
		type : 'POST',
		url : url
	    });
	},
	/**
	 * Удаление рассказа
	 * 
	 * @param event
	 *                event Событие
	 */
	remove : function(event) {
	    event.stopImmediatePropagation();
	    event.preventDefault();
	    if (!(pages.story_view.regex.test(window.location.pathname))) {
		var url = '/ajax' + $(this).attr('href');
		$.post(url, function(data) {
		    $('#story_' + data).slideUp('slow').remove();
		}).success(function() {
		    $('.modal').modal('hide').remove();
		});
	    } else {
		$('.modal').modal('hide').remove();
		window.location = '/';
	    }
	},
    },
    /**
     * Работа с главами
     */
    chapter : {
	/**
	 * Удаление главы по AJAX
	 * 
	 * @param event
	 *                event Событие
	 */
	remove : function(event) {
	    event.stopImmediatePropagation();
	    event.preventDefault();
	    var url = '/ajax' + $(this).attr('href');
	    $('#sortable_chapters').sortable('destroy');
	    $.post(url, function(data) {
		$('#chapter_' + data).slideUp('slow').remove();
	    }).success(function() {
		$('.modal').modal('hide').remove();
		listeners.chapter.sortability();
	    });
	},
    },
    /**
     * Работа с авторами
     */
    author : {
	/**
	 * Одобрение автора
	 * 
	 * @param response
	 *                int ID рассказа
	 */
	approve : function(response) {
	    var btn = $('#author_approve');
	    if (btn.hasClass('btn-primary')) {
		var text = 'Не проверен';
	    } else {
		var text = 'Проверен';
	    }
	    btn.text(text).toggleClass('btn-primary');
	}
    }
}

/**
 * События
 */

var listeners = {
    story : {
	// Удаление
	remove : function() {
	    $(document).on('click', '.story_delete', ajax.modal);
	    $(document).on('click', '.ajax_story_delete:visible', ajax.story.remove);
	},
	// Одобрение
	approve : function() {
	    $('.story_approve').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, ajax.story.approve);
	    });
	},
	// Публикация
	publish : function() {
	    $('.story_publish').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, ajax.story.publish);
	    });
	},
	// Закладки
	bookmark : function() {
	    $('.story_bookmark').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, ajax.story.bookmark);
	    });
	},
	// Избранное
	favorite : function() {
	    $('.story_favorite').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, ajax.story.favorite);
	    });
	},
	// Переключение размера и типа шрифта
	style : function() {
	    var font_selector = $('.select-font');
	    var size_selector = $('.select-size');
	    var chapter_text = $('.chapter-text');
	    font_selector.change(function() {
		if (font_selector.val() == '1')
		    chapter_text.removeClass('mono-font serif-font');
		else if (font_selector.val() == '2')
		    chapter_text.removeClass('mono-font').addClass('serif-font');
		else if (font_selector.val() == '3')
		    chapter_text.removeClass('serif-font').addClass('mono-font');
	    });
	    size_selector.change(function() {
		if (size_selector.val() == '1')
		    chapter_text.removeClass('small-font big-font');
		else if (size_selector.val() == '2')
		    chapter_text.removeClass('big-font').addClass('small-font');
		else if (size_selector.val() == '3')
		    chapter_text.removeClass('small-font').addClass('big-font');
	    });
	},
	// Голосование
	vote : function() {
	    $('#vote-up').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		ajax.story.vote(url)
	    });
	    $('#vote-down').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		ajax.story.vote(url)
	    });
	},
    },
    comment : {
	// Управление AJAX-пагинацией
	pagination : function() {
	    $('#ajax_next_comment').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		ajax.comment.load(url);
	    });
	    $('#ajax_prev_comment').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		ajax.comment.load(url);
	    });
	},
	// Добавление комментария
	add : function() {
	    $(document).on('click', '.comment_add', ajax.modal);
	},
	// Редактирование комментария
	edit : function() {
	    $(document).on('click', '.comment_edit', ajax.modal);
	},
	// Отправка комментария
	send : function() {
	    $(document).on('click', '.modal .comment_submit', ajax.comment.send);
	},
	// Удаление комментария
	remove : function() {
	    $(document).on('click', '.comment_delete', ajax.modal);
	    $(document).on('click', '.ajax_comment_delete:visible', ajax.comment.remove);
	},
    },
    chapter : {
	remove : function() {
	    $(document).on('click', '.chapter_delete', ajax.modal);
	    $(document).on('click', '.ajax_chapter_delete:visible', ajax.chapter.remove);
	},
	sortability : function() {
	    $('#sortable_chapters').sortable({
		update : function() {
		    $.ajax({
			data : $('#sortable_chapters').sortable('serialize'),
			type : 'POST',
			url : 'ajax'
		    });
		}
	    });
	},

    },
    author : {
	// Одобрение
	approve : function() {
	    $('#author_approve').click(function(event) {
		event.stopImmediatePropagation();
		event.preventDefault();
		var url = '/ajax' + $(this).attr('href');
		$.post(url, ajax.author.approve);
	    });
	}
    },
    misc : {
	characters : function() {
	    $(".character-item").click(function() {
		if (Boolean($(this).children('input:checked').length)) {
		    $(this).children('img').removeClass('ui-selected');
		    $(this).children('input').removeAttr('checked');
		} else {
		    $(this).children('img').addClass("ui-selected");
		    $(this).children('input').attr('checked', 'checked');
		}
	    });
	},
	search : function() {
	    $('input[name="characters_select"][checked="checked"]').parent().children('img').addClass('ui-selected');
	    $("#reset_search").click(function() {
		$('input:checked').removeAttr('checked');
		$('button').removeClass('active');
		$('img').removeClass('ui-selected');
		document.getElementById('appendedInputButtons').setAttribute('value', '');
		$('.span8').slideUp();
	    });
	}
    }
}

var pages = {
    index : {
	regex : new RegExp('^/$'),
	action : function() {
	    $('#nav_index').addClass('active');
	    for ( var listener in listeners.story) {
		listeners.story[listener]();
	    }
	}
    },
    story_view : {
	regex : new RegExp('^/story/[0-9]+/(?:comments/page/[0-9]+/)?$'),
	action : function() {
	    $('#id_text').markItUp(mySettings)
	    for ( var listener in listeners.story) {
		listeners.story[listener]();
	    }
	    for ( var listener in listeners.comment) {
		listeners.comment[listener]();
	    }
	    stuff.panel();
	    if ($('#wrapper').hasClass('nsfw')) {
		$('#nsfwModal').modal();
	    }
	}
    },
    story_add : {
	regex : new RegExp('^/story/add/$'),
	action : function() {
	    $('#nav_story_add').addClass('active');
	    $('#id_text').markItUp(mySettings);
	    $('#id_notes').markItUp(mySettings);
	    $('.character-item input[checked="checked"]').prev().addClass('ui-selected');
	}
    },
    story_edit : {
	regex : new RegExp('^/story/[0-9]+/edit/$'),
	action : function() {
	    $('#id_text').markItUp(mySettings);
	    $('#id_notes').markItUp(mySettings);
	    $('.character-item input[checked="checked"]').prev().addClass('ui-selected');
	    for ( var listener in listeners.chapter) {
		listeners.chapter[listener]();
	    }
	}
    },
    chapter_view : {
	regex : new RegExp('^/story/[0-9]+/chapter/(?:[0-9]+|all)/$'),
	action : function() {
	    stuff.panel();
	    if ($('#wrapper').hasClass('nsfw')) {
		$('#nsfwModal').modal();
	    }
	}
    },
    chapter_add : {
	regex : new RegExp('^/story/[0-9]+/chapter/add/$'),
	action : function() {
	    $('#id_text').markItUp(mySettings);
	    $('#id_notes').markItUp(mySettings);
	}
    },
    chapter_edit : {
	regex : new RegExp('^/chapter/[0-9]+/edit/$'),
	action : function() {
	    $('#id_text').markItUp(mySettings);
	    $('#id_notes').markItUp(mySettings);
	}
    },
    comment_add : {
	regex : new RegExp('^/story/[0-9]+/comment/add/$'),
	action : function() {
	    $('#id_text').markItUp(mySettings);
	}
    },
    comment_edit : {
	regex : new RegExp('^/story/[0-9]+/comment/[0-9]+/edit/$'),
	action : function() {
	    $('#id_text').markItUp(mySettings);
	}
    },
    author_overview : {
	regex : new RegExp('^/accounts/[0-9]+/(?:comments/page/[0-9]+/)?$'),
	action : function() {
	    $('#nav_author_overview').addClass('active');
	    listeners.author.approve();
	    listeners.comment.pagination();
	    for ( var listener in listeners.story) {
		listeners.story[listener]();
	    }
	}
    },
    author_dashboard : {
	regex : new RegExp('^/accounts/profile/(?:comments/page/[0-9]+/)?$'),
	action : function() {
	    $('#nav_author_dashboard').addClass('active');
	    listeners.author.approve();
	    listeners.comment.pagination();
	    for ( var listener in listeners.story) {
		listeners.story[listener]();
	    }
	}
    },
    registration : {
	regex : new RegExp('^/accounts/registration/(.+)?'),
	action : function() {
	    $('#nav_registration').addClass('active');
	}
    },
    search : {
	regex : new RegExp('^/search/(.+)?'),
	action : function() {
	    $('#nav_search').addClass('active');
	    listeners.misc.characters();
	    listeners.misc.search();
	    for ( var listener in listeners.story) {
		listeners.story[listener]();
	    }
	}
    },
    favorites : {
	regex : new RegExp('^/accounts/[0-9]+/favorites/(.+)?'),
	action : function() {
	    $('#nav_favorites').addClass('active');
	    for ( var listener in listeners.story) {
		listeners.story[listener]();
	    }
	}
    },
    bookmarks : {
	regex : new RegExp('^/bookmarks/(.+)?'),
	action : function() {
	    $('#nav_bookmarks').addClass('active');
	    for ( var listener in listeners.story) {
		listeners.story[listener]();
	    }
	}
    },
    submitted : {
	regex : new RegExp('^/submitted/(.+)?'),
	action : function() {
	    $('#nav_submitted').addClass('active');
	    for ( var listener in listeners.story) {
		listeners.story[listener]();
	    }
	}
    },
    help : {
	regex : new RegExp('^/help/$'),
	action : function() {
	    $('#nav_help').addClass('active');
	    $('a.tab_inline[data-toggle="tab"]').click(function() {
		var href = $($(this)['context']).attr('href');
		$('.nav-simple li').removeClass('active');
		$('.nav-simple li a[href="' + href + '"]').parent().addClass('active');

	    });
	}
    },
    terms : {
	regex : new RegExp('^/terms/$'),
	action : function() {
	    $('#nav_terms').addClass('active');
	}
    },
}

var stuff = {
    // Действия на каждом типе страниц
    page : function() {
	for ( var page in pages) {
	    if (pages[page].regex.test(window.location.pathname)) {
		pages[page].action()
	    }
	}
    },
    // Ротатор шапок
    logo : function() {
	var len = 8
	if ($.cookie('stories_gr') == null) {
	    var stories_gr = Math.floor(Math.random() * len) + 1;
	    $.cookie('stories_gr', stories_gr, {
		expires : 1
	    });
	} else {
	    var stories_gr = $.cookie('stories_gr');
	}
	var new_image = "url(/static/i/logopics/logopic-" + stories_gr + ".jpg)";
	$('.logopic').css('background-image', new_image);
    },
    // Плавающая панелька
    panel : function() {
	var storypanel = $('#story_panel');
	var storypanelHomeY = storypanel.offset().top;
	var isFixed = false;
	var $w = $(window);
	$w.scroll(function() {
	    var scrollTop = $w.scrollTop();
	    var shouldBeFixed = scrollTop > storypanelHomeY;
	    $('#story_panel').css('opacity: 1');
	    $("#wrapper").hover(function() {
		if (isFixed) {
		    $(this).find("#story_panel").stop().animate({
			opacity : 1
		    });
		}
	    }, function() {
		if (isFixed) {
		    $(this).find("#story_panel").stop().animate({
			opacity : 0
		    });
		}
	    });
	    // Когда скролл есть
	    if (shouldBeFixed && !isFixed) {
		storypanel.css({
		    position : 'fixed',
		    top : 0,
		    left : storypanel.offset().left + 12,
		    width : storypanel.width(),
		    opacity : 0
		});
		isFixed = true;
	    }
	    // Когда скролла нет
	    else if (!shouldBeFixed && isFixed) {
		storypanel.css({
		    position : 'static',
		    opacity : 1.0
		});
		isFixed = false;
	    }
	});
    },
    // Обработка состояний BootStrap Elements
    bootstrap : function() {
	var group = $(this);
	var buttons_container = $('.buttons-visible', group)
	var data_container = $('.buttons-data', group)

	if (group.hasClass('checkbox')) {
	    var type = 'checkbox'
	} else if (group.hasClass('radio')) {
	    var type = 'radio'
	}
	// Обработка проставленных заранее чекбоксов и радиоселектов
	$('input', data_container).each(function() {
	    var input = $(this);
	    value = input.attr('value')
	    checked = Boolean(input.attr('checked'))
	    if (checked) {
		buttons_container.children('button[value=' + value + ']').addClass('active');
	    }
	});
	// Onclick-обработчик
	$('button', buttons_container).each(function() {
	    var button = $(this);
	    button.on('click', function() {
		value = button.attr('value');
		if (type == 'checkbox') {
		    input = $('input:checkbox[value=' + value + ']', data_container);
		    selected = Boolean($('input:checked[value=' + value + ']', data_container).length);
		    selected ? input.removeAttr('checked') : input.attr('checked', 'checked');
		} else if (type == 'radio') {
		    input = $('input:radio[value=' + value + ']', data_container);
		    all_inputs = $('input:radio', data_container);
		    all_inputs.removeAttr('checked');
		    input.attr('checked', 'checked');
		}
	    });
	});
    },
    // Конфигурация заголовка AJAX-запроса с CSRF Cookie
    ajaxsetup : function() {
	$.ajaxSetup({
	    cache : false,
	    crossDomain : false,
	    error : ajax.errorhandler,
	    beforeSend : function(request) {
		request.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
	    }
	});
    },
    carousel : function() {
	$("#slides").slidesjs({
	    width : 524,
	    height : 200,
	    navigation : {
		active : true,
		effect : "fade",
	    },
	    pagination : {
		active : false,
	    },
	    effect : {
		slide : {
		    speed : 1500,
		},
		fade : {
		    speed : 300,
		    crossfade : false,
		}
	    },
	    play : {
		active : false,
		effect : "fade",
		interval : 5000,
		auto : true,
		swap : true,
		pauseOnHover : true,
		restartDelay : 2500
	    }
	});
	$('.slidesjs-previous').html('<img src="/static/i/arrow-left.png" />');
	$('.slidesjs-next').html('<img src="/static/i/arrow-right.png" />');
    }
}
// При загрузке страницы
$(function() {
    stuff.logo();
    stuff.ajaxsetup();
    stuff.carousel();
    $('.bootstrap').each(stuff.bootstrap);
    stuff.page();
});