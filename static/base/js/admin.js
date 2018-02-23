// Admin-Specific js Functions
// URL paths used for js routing
const u_api = "/admin/main/";
const u_proj = "project/";
const u_imgGet = "/image/get/";
const u_imgAdd = "/image/add/";
const u_resList = "/resume/list";

$(document).ready(function ready() {
    // if there errors in the create or edit form, show the new project dropdown
    errors = $('#formErrors').val()
    edit_errors = $('#formEditErrors').val()
    if (errors == "True") {
        $('#form_body').collapse({
            toggle: true
        })
    }
    if (edit_errors == "True") {
        $('#projectEdit').modal('show');
    }


    // capitalize first letter of each word
    function capitalize_words(s) {
        s = s.toLowerCase();
        words = s.split(" ");
        s = "";
        for (let i=0; i<words.length; i++) {
            word = words[i];
            word_first = word[0];
            word_first = word_first.toUpperCase();
            word = word_first + word.slice(1) + " ";
            s += word
        }
        s = s.trim();
        return s;
    }

    // capitalize all letters in string
    function all_caps(s) {
        return s.toUpperCase();
    }

    // alert user and confirm before removing item
    // this function does not execute the remove function
    // it will return the user response (true or false)
    function confirm_remove(event, elementId) {
        elementId = "#" + elementId;
        var type = $(elementId).attr("x-type");  // type of record
        type = capitalize_words(type);
        var name = $(elementId).attr("x-name");  // name of record
        name = all_caps(name);

        var msg = `You are about to delete the ${type}, ${name}. \n\nThis cannot be undone. Would you like to continue?`;
        return confirm(msg);
    }

    // on clicking any remove action, require confirmation
    $(document).on('click', '.destroy_action', function (event) {
        event.preventDefault();             // Prevent default anchor click behavior
        var href = $(this).attr("href");    // url (href)
        var id = $(this).attr('id');
        if (confirm_remove(event, id)) {
            window.location.href = href;
        }
    });


    // enable all popover tooltips on view
    $('[data-toggle="tooltip"]').tooltip();
    $('[data-toggle="popover"]').popover();


    // Skill Form multiple select by checkbox
    $(document).on('click', '.onClickSkillChoice', function (event) {
        var label_id = $(this).attr('id');
        // determine which form was clicked
        var newFormLabel = "_lbNew",
            newFormCheckbox = "_newCheck",
            newSelectOption = "skillOptionNew_",
            editFormLabel = "_lbEdt",
            editFormCheckbox = "_editCheck",
            editSelectOption = "skillOptionEdit_",
            thisSuffix = label_id.substr(label_id.length - 6),
            input_id,
            checkbox,
            selection

        if (thisSuffix == newFormLabel) {
            input_id = label_id.replace(newFormLabel, "");
            checkbox = input_id + newFormCheckbox;
            selection = newSelectOption + input_id;
        }
        else {
            input_id = label_id.replace(editFormLabel, "");
            checkbox = input_id + editFormCheckbox;
            selection = editSelectOption + input_id;
        }

        // toggle the checked attribute
        $("#" + checkbox).attr('checked', !$("#" + checkbox).attr('checked'));
        // change the label style of the selected element
        $("#" + label_id).toggleClass('choiceSelected');
        // select or unselect the skill from the hidden select input field
        var selectedVal = $("#" + selection).attr('selected');
        $("#" + selection).attr('selected', !selectedVal);
    });


    // Convert form data to json-ready object of serialized strings
    function formify(form) {
        let form_data_serialize = form.serializeArray();
        let form_data_object = new FormData();
        for (let i=0; i < form_data_serialize.length; i++) {
            // form_data_object[form_data_serialize[i]['name']] = form_data_serialize[i]['value'];
            form_data_object.append(form_data_serialize[i]['name'], form_data_serialize[i]['value']);
        }
        return form_data_object;
    }


    // Read Image Input and Show in Target HTML Element
    function readURL(input, target_img) {
        if (input || (input.files && input.files[0])) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $(target_img).attr('src', e.target.result);
            }
            if (input.files && input.files[0]) {
                reader.readAsDataURL(input.files[0]);
            }
            else {
                reader.readAsDataURL(input);
            }
        }
    }


    // AJAX -- Fetch() GET Handler
    function fetch_get_handler(
        get_url,        // get route string
        res_container,  // container for HTML response as jQuery selected object
        context,        // additional data used in callback (optional)
        callback,       // optional callback to complete upon receiving response
    ) {
        fetch(get_url, {
            credentials: 'include'
        })
        .then(response => response.text())
        .then(response => {
            if (res_container && res_container != "") { 
                res_container.html(response);
            }
        })
        .then(response => {
            if (callback && typeof (callback) === 'function') { callback(context); }
        })
    }


    // AJAX -- Fetch() POST/PUT Handler
    function fetch_post_handler(
        post_url,       // post route string
        method,         // POST / PUT method
        csrftoken,      // CSRF token generated on the Django form
        form_data,      // body data of FormData type
        form_selector,  // form as jQuery selected object
        context,        // additional data used in callback (optional)
        response_modal_id,  // modal element id to display response
        callback_success,   // optional callback to complete upon receiving response
        callback_error,     // callback after errors
        callback_all,       // callback after all cases
    ) {
        fetch(post_url, {
            method: method,
            body: form_data,
            credentials: 'include',
            headers: new Headers({
                'X-CSRFToken': csrftoken,
            })
        })
        .then(response => {
            let xhFormErrors = response.headers.get('X-Form-Errors');
            response.text().then(html_response => {
                if (xhFormErrors == "True") {
                    // there were errors in the form
                    // display the form again with errors
                    form_selector.html(html_response);
                    if (callback_error && typeof(callback_error) === 'function') { callback_error(); }
                }
                else {
                    // form submitted successfully
                    if (response_modal_id && response_modal_id != "") {
                        $(document.body).append(html_response);
                        $('#' + response_modal_id).modal('show');
                    }
                    if (callback_success && typeof (callback_success) === 'function') { callback_success(context); }
                }
            });
        })
        .then(response => { 
            if (callback_all && typeof (callback_all) === 'function') { callback_all(); }
        });
    }


    // AJAX -- get all images -- this routine is used frequently
    function get_all_project_images(projId) {
        url_img_all = u_api + u_proj + projId + u_imgGet;
        img_container = $('#projectImageList')
        fetch_get_handler(
            get_url=url_img_all,
            res_container=img_container,
        );
    }


    // AJAX -- get project edit form partial html [1 of 2 handlers]
    $('.project-edit-link').click(function(event) {
        event.preventDefault();
        get_url = $(this).attr("href");
        get_proj = $(this).attr("proj");
        callback = function(get_proj) {
            $('#projectEditTitle').text(get_proj);
            $('#projectEdit').modal('show');
        }
        fetch_get_handler(
            get_url=get_url,
            res_container=$('#edit-form'),
            context=get_proj,
            callback=callback
        );
    });
    // AJAX -- get project images and form partial html [2 of 2 handlers]
    $('.project-edit-link').click(function (event) {
        event.preventDefault();
        get_url = $(this).attr("href");
        get_proj = $(this).attr("proj");
        projId = $(this).attr("projId");
        url_img_form = u_api + u_proj + projId + u_imgAdd;

        $('#projectImageTitle').text(get_proj);
        get_all_project_images(projId);

        fetch_get_handler(
            get_url=url_img_form,
            res_container=$('#projectImageForm'),
        );
    });
    
    
    // AJAX -- post project edit form and await response
    $(document).on('click', '#project-edit-submit', function (event) {
        $('#edit-project-form').submit();
    });
    $(document).on('submit', '#edit-project-form', function(event) {
        // hide edit form and wait for AJAX response
        event.preventDefault();
        $('#projectEdit').modal('hide');
        $('#projectEdit').on('hidden.bs.modal', function() {
            // remove event handler for edit modal hide
            $('#projectEdit').off('hidden.bs.modal')
            var contextForm = $('#edit-project-form');
            var post_url = contextForm.attr('action');
            var post_type = contextForm.attr('method');
            var form_data = formify(contextForm);   // convert to FormData object
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]", contextForm).val();

            function case_success() {
                $('#projectEditRes').modal('show');
            }
            function case_error() {
                $('#projectEdit').modal('show');
            }

            fetch_post_handler(
                post_url = post_url,
                method = post_type,
                csrftoken = csrftoken,
                form_data = form_data,
                form_selector = contextForm,
                context = "",
                response_modal_id = "projectEditRes",
                callback_success = case_success,
                callback_error = case_error,
                callback_all = "",
            );
        });
    });


    // AJAX -- post image add form and await response
    $(document).on('submit', '#img-add-form', function (event) {
        // disable submit button to avoid multiple uploads
        event.preventDefault();
        $('#project-img-add').prop('disabled', true);
        $('#projectEdit').modal('hide');
        $('#projectEdit').on('hidden.bs.modal', function () {
            // remove event handler for edit modal hide
            $('#projectEdit').off('hidden.bs.modal')

            var contextForm = $('#img-add-form');
            var post_url = contextForm.attr('action');
            var post_type = contextForm.attr('enctype');
            var projId = jQuery("[name=project]", contextForm).val();
            var form_data = formify(contextForm);   // convert to FormData object
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]", contextForm).val();
            var img_file = $('input:file')[0].files[0]; // select uploaded image
            form_data.append('img_url', img_file);      // append to FormData

            function case_all() {
                $('#project-img-add').prop('disabled', false);    // reenable submit button
                $('#projectEdit').modal('show');
            }
            function case_success(projId) {
                get_all_project_images(projId);
                document.getElementById("img-add-form").reset();
            }

            fetch_post_handler(
                post_url=post_url,
                method="POST",
                csrftoken=csrftoken,
                form_data=form_data,
                form_selector=contextForm,
                context=projId,
                response_modal_id="projectEditRes",
                callback_success=case_success,
                callback_error=null,
                callback_all=case_all,
            );
        });
    });


    // AJAX -- get image edit form
    $(document).on('click', '.edit-img-link', function(event) {
        event.preventDefault();
        var get_url = $(this).attr('href');
        $('#projectEdit').modal('hide');
        $('#projectEdit').on('hidden.bs.modal', function() {
            // remove event handler for edit modal hide
            $('#projectEdit').off('hidden.bs.modal')
            fetch_get_handler(
                get_url=get_url,
                res_container=$('#projectModal'),
                context="",
                callback=function() {
                    $('.edit-img-remove').off('click');
                    $('#modal').modal('show');
                }
            );
        });
    });

    // AJAX -- post image edit form
    $(document).on('submit', '#img-edit-form', function(event) {
        // disable submit button to avoid multiple uploads
        event.preventDefault();
        $('#project-img-edit').prop('disabled', true);
        $('#img-edit-form').prop('disabled', true);

        var contextForm = $('#img-edit-form');
        var post_url = contextForm.attr('action');
        var post_type = contextForm.attr('enctype');
        var projId = jQuery("[name=project]", contextForm).val();
        var form_data = formify(contextForm);   // convert to FormData object
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]", contextForm).val();

        function case_error() {
            $('#project-img-edit').prop('disabled', false);    // reenable submit button
            $('#img-edit-form').prop('disabled', false);
        }
        function case_success(projId) {
            $('#modal').modal('hide');
            $('#projectEdit').modal('show');
            get_all_project_images(projId);
        }

        fetch_post_handler(
            post_url=post_url,
            method="POST",
            csrftoken=csrftoken,
            form_data=form_data,
            form_selector=contextForm,
            context=projId,
            response_modal_id="projectEditRes",
            callback_success=case_success,
            callback_error=case_error,
            callback_all="",
        );
    });


    // AJAX -- Modify Featured Image on View
    $(document).on('click', '.set-img-feature', function(event) {
        event.preventDefault();
        var post_url = $(this).attr('href');
        var imgId = $(this).attr('img');
        var img_url = $(this).attr('img-src');
        var form_id = '#set-img-feature-form-' + imgId
        var contextForm = $(form_id);
        var projId = jQuery("[name=project]", contextForm).val();
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]", contextForm).val();
        
        // modify logo image on the project list
        var logo_id = '#proj-list-logo-' + projId;
        $(logo_id).attr('src', '/media/' + img_url);

        $('#projectEdit').modal('hide');
        $('#projectEdit').on('hidden.bs.modal', function (event) {
            // remove event handler for edit modal hide
            $('#projectEdit').off('hidden.bs.modal');

            function case_success(projId) {
                $('#projectEdit').modal('show');
                get_all_project_images(projId);
            }

            fetch_post_handler(
                post_url = post_url,
                method = "POST",
                csrftoken = csrftoken,
                form_data = "",
                form_selector = contextForm,
                context = projId,
                response_modal_id = "",
                callback_success = case_success,
                callback_error = "",
                callback_all = "",
            );
        });
    })


    // AJAX -- remove image and refresh images on view
    $(document).on('click', '.edit-img-remove', function (event) {
        event.preventDefault();
        var id = $(this).attr("id");
        if (confirm_remove(event, id)) {
            var get_url = $(this).attr('href');
            var projId = $(this).attr('proj');

            function callback(projId) {
                // upon img removal, refresh image view
                get_all_project_images(projId);
                $('.edit-img-remove').off('click') 
            }
            fetch_get_handler(
                get_url=get_url,
                res_container="",
                context=projId,
                callback=callback
            )
        }
        else {
            $('.edit-img-remove').off('click')  // re-enable clicks
        }
    });


    // --- START SKILL LOGO --- //
    function disable_skill_links() {
        $('.skill-logo-edit').addClass('disabled');
        $('.skill-logo-edit').attr('aria-disabled', true);
        $('.skill-edit').addClass('disabled');
        $('.skill-edit').attr('aria-disabled', true);
        $('.skill-destroy').addClass('disabled');
        $('.skill-destroy').attr('aria-disabled', true);
    }

    function enable_skill_links() {
        $('.skill-logo-edit').removeClass('disabled');
        $('.skill-logo-edit').attr('aria-disabled', false);
        $('.skill-edit').removeClass('disabled');
        $('.skill-edit').attr('aria-disabled', false);
        $('.skill-destroy').removeClass('disabled');
        $('.skill-destroy').attr('aria-disabled', false);
    }

    function remove_skill_logo_form() {
        $('#skill-logo-form').remove();
    }


    // AJAX -- get skill logo edit form
    $(document).on('click', '.skill-logo-edit', function(event) {
        event.preventDefault();
        var get_url = $(this).attr('href');
        if ($(this).hasClass('disabled')) {
            return;
        }

        var id = $(this).attr('skillId');
        var skill_id = "#skill_" + id.toString();
        // create container to hold logo form
        html = "<th colspan='6' id='skill-logo-form' class='col-sm-12 mx-0 px-0'></th>"
        $(skill_id).after(html);
        fetch_get_handler(
            get_url=get_url,
            res_container=$('#skill-logo-form'),
            context="",
            callback=function() {
                disable_skill_links();
            }
        );
    });
    
    // Select Skill Logo File
    $(document).on('change', '#skill-logo-file', function(event) {
        readURL(this, '#skill-logo-show');
    })

    // Cancel Skill Logo Edit
    $(document).on('click', '#skill-logo-cancel', function(event) {
        enable_skill_links();
        remove_skill_logo_form();
    })


    // AJAX -- post new skill logo
    $(document).on('submit', '#skill-logo-form', function(event) {
        // disable submit button to avoid multiple uploads
        event.preventDefault();
        $('#skill-logo-add').prop('disabled', true);
        $('#skill-logo').prop('disabled', true);

        var contextForm = $('#skill-logo');
        var post_url = contextForm.attr('action');
        var post_type = contextForm.attr('enctype');
        var skillId = contextForm.attr('skillId');
        var form_data = formify(contextForm);   // convert to FormData object
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]", contextForm).val();
        var img_file = $('input:file')[0].files[0]; // select uploaded image
        form_data.append('img', img_file);      // append to FormData

        function case_all() {
            $('#skill-logo-add').prop('disabled', false);   // reenable submit
            $('#skill-logo').prop('disabled', false);       // reenable submit
        }
        function case_success(context) {
            el_img = "#skill-logo-" + context['skillId'];
            readURL(context['img_file'], el_img);
            enable_skill_links();
            remove_skill_logo_form();
            document.getElementById("skill-logo").reset();
        }

        fetch_post_handler(
            post_url=post_url,
            method="POST",
            csrftoken=csrftoken,
            form_data=form_data,
            form_selector=contextForm,
            context={'skillId':skillId, 'img_file':img_file},
            response_modal_id="projectEditRes",
            callback_success=case_success,
            callback_error=null,
            callback_all=case_all,
        );
    });


    // AJAX -- remove skill logo and get form again
    $(document).on('click', '#skill-logo-remove', function(event) {
        event.preventDefault();
        if ($(this).hasClass('disabled')) {
            return;
        }
        var id = $(this).attr('id');
        if (confirm_remove(event, id)) {
            var get_url = $(this).attr('href');
            var skill_id = $('#skill-logo').attr('skillId');

            function callback(skill_id) {
                var el_img = '#skill-logo-' + skill_id;
                $(el_img).attr('src', '');
            }

            fetch_get_handler(
                get_url=get_url,
                res_container=$('#skill-logo-form'),
                context=skill_id,
                callback=callback
            );
        }
    });


    // AJAX -- get resume list
    function get_resume_list() {
        var get_url = u_api + u_resList;
        fetch_get_handler(
            get_url=get_url,
            res_container=$("#resume-list"),
            context="",
            callback=null
        );
    }


    // AJAX -- upload resume
    $(document).on('submit', '#resume-upload-form', function(event) {
        // disable submit button to avoid multiple uploads
        event.preventDefault();
        $('#resume-upload-submit').prop('disabled', true);

        var contextForm = $('#resume-upload-form');
        var post_url = contextForm.attr('action');
        var post_type = contextForm.attr('enctype');
        var form_data = formify(contextForm);   // convert to FormData object
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]", contextForm).val();
        var up_file = $('input:file')[0].files[0]; // select uploaded image
        form_data.append('res_file', up_file);      // append to FormData

        function case_all() {
            $('#resume-upload-submit').prop('disabled', false);   // reenable submit
        }
        function case_success(context) {
            get_resume_list()
            document.getElementById("resume-upload-form").reset();
        }

        fetch_post_handler(
            post_url=post_url,
            method="POST",
            csrftoken=csrftoken,
            form_data=form_data,
            form_selector=contextForm,
            context="",
            response_modal_id="projectEditRes",
            callback_success=case_success,
            callback_error=null,
            callback_all=case_all,
        );
    });


    // remove temporary modals after hidden
    $('body').on('hidden.bs.modal', '#projectEditRes', function () {
        $('#projectEditRes').remove();
    });
    $('body').on('hidden.bs.modal', '#modal', function () {
        $('#modal').remove();
    });
});

