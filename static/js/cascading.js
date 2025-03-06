$(document).ready(function() {
    // Function to update the school code field
    function updateSchoolCode(schoolId) {
        if (schoolId) {
            $.ajax({
                url: '/ajax/school-code/',
                data: {
                    'school_id': schoolId
                },
                dataType: 'json',
                success: function(data) {
                    $('#id_school_code').val(data.code);
                }
            });
        } else {
            $('#id_school_code').val('');
        }
    }

    // When state is changed, update districts
    $('#id_state').change(function() {
        var stateId = $(this).val();
        
        // Clear dependent dropdowns
        $('#id_district').empty().append('<option value="">----------</option>');
        $('#id_block').empty().append('<option value="">----------</option>');
        $('#id_school').empty().append('<option value="">----------</option>');
        $('#id_school_code').val('');
        
        if (stateId) {
            $.ajax({
                url: '/ajax/districts/',
                data: {
                    'state_id': stateId
                },
                dataType: 'json',
                success: function(data) {
                    $.each(data, function(index, item) {
                        $('#id_district').append(
                            $('<option></option>').val(item.id).text(item.name)
                        );
                    });
                }
            });
        }
    });

    // When district is changed, update blocks
    $('#id_district').change(function() {
        var districtId = $(this).val();
        
        // Clear dependent dropdowns
        $('#id_block').empty().append('<option value="">----------</option>');
        $('#id_school').empty().append('<option value="">----------</option>');
        $('#id_school_code').val('');
        
        if (districtId) {
            $.ajax({
                url: '/ajax/blocks/',
                data: {
                    'district_id': districtId
                },
                dataType: 'json',
                success: function(data) {
                    $.each(data, function(index, item) {
                        $('#id_block').append(
                            $('<option></option>').val(item.id).text(item.name)
                        );
                    });
                }
            });
        }
    });

    // When block is changed, update schools
    $('#id_block').change(function() {
        var blockId = $(this).val();
        
        // Clear dependent dropdowns
        $('#id_school').empty().append('<option value="">----------</option>');
        $('#id_school_code').val('');
        
        if (blockId) {
            $.ajax({
                url: '/ajax/schools/',
                data: {
                    'block_id': blockId
                },
                dataType: 'json',
                success: function(data) {
                    $.each(data, function(index, item) {
                        $('#id_school').append(
                            $('<option></option>').val(item.id).text(item.name)
                        );
                    });
                }
            });
        }
    });

    // When school is changed, update school code
    $('#id_school').change(function() {
        var schoolId = $(this).val();
        updateSchoolCode(schoolId);
    });
});