// Admin-Specific js Functions
$(document).ready(function () {
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


    // on clicking any remove action, require confirmation
    $(document).on('click', '.destroy_action', function (event) {
        // Prevent default anchor click behavior
        event.preventDefault();

        // Store hash (href)
        var href_store = $(this).attr("href");

        // Confirm Action
        var msg = "You are about to delete a record. This cannot be undone. Would you like to continue?";
        var user_confirm = confirm(msg);
        if (user_confirm) {
            window.location.href = href_store
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


    function formify(form) {
        let form_data_serialize = form.serializeArray();
        let form_data_object = new FormData();
        for (let i=0; i < form_data_serialize.length; i++) {
            // form_data_object[form_data_serialize[i]['name']] = form_data_serialize[i]['value'];
            form_data_object.append(form_data_serialize[i]['name'], form_data_serialize[i]['value']);
        }
        // let form_data_stringify = JSON.stringify(form_data_object);
        return form_data_object;
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
        url_img_all = "admin/project/" + projId + "/image/get";
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

        projId = get_url.replace("/admin/project/edit/", "");
        url_img_form = "admin/project/" + projId + "/image/add";

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
        $('.edit-img-remove').on('click', function(e) {
            // disable link to avoid multiple removal clicks
            e.preventDefault();
            return false;
        });
        var msg = "You are about to delete this image. This cannot be undone. Would you like to continue?";
        var user_confirm = confirm(msg);
        if (user_confirm) {
            var get_url = $(this).attr('href');
            var projId = $(this).attr('proj');

            function callback(projId) {
                // upon img removal, refresh image view
                url_img_all = "admin/project/" + projId + "/image/get";
                fetch_get_handler(
                    get_url=url_img_all,
                    res_container=$('#projectImageList'),
                    context="",
                    callback=function() { 
                        $('.edit-img-remove').off('click') 
                    }
                )
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


    // remove tempoarary modals after hidden
    $('body').on('hidden.bs.modal', '#projectEditRes', function () {
        $('#projectEditRes').remove();
    });
    $('body').on('hidden.bs.modal', '#modal', function () {
        $('#modal').remove();
    });
});
