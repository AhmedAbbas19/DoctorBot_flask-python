$(document).ready(function(){

    // nice scroll Library
    $('html,.ques').niceScroll();

    $('#myDropdown').hide();
    $('[data-toggle="tooltip"]').tooltip();

    // Responsive Image Maps jQuery Plugin
    $('img[usemap]').rwdImageMaps();

    $('#myInput').on('keyup',function(){
        if($('#myInput').val()==""){
            $('#myDropdown').hide();
        }else{
            $('#myDropdown').fadeIn();
        }
    });
    
    $('#myInput').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $('#myDropdown div p').filter(function() {
            $(this).parent().toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });


    $(document).on('click','.sympRemove',function() {
        $(this).closest('.addedSysmp').remove();
    });

    $(document).on('click','.closeOrgan',function() {
        $(this).closest('#organDropdown').fadeOut();
        $
    });

    $(document).on('click','.closeDis',function() {
        $(this).closest('.diseses-data').css('right','-2500px');
        $
    });

    
    $(document).on('click','.addBtn',function(){
        var symp = $(this).prev().text();
        $('#allSymps').append('<label class="addedSysmp">'+symp+'<input type="text" name="sym[]" value="'+symp+'" hidden><i class="fa fa-close sympRemove"></i></label>');
    });


    $('#nxt-info').on('click',function(){
        $(this).hide();
        $('.info .gender').hide();
        $('.info .age').css('display','block');
        $('#info-submit').css('display','block');
    });

    $('#myRange').on('input',function() {
        $('#age-value').html(this.value);
    });

    $('select[name=acc_type]').on('change',function(){
        if ($(this).val() == 'doctor' ){
            $('#doctorSpec').fadeIn();
        } 
        else{
            $('#doctorSpec').fadeOut();
        }
    });

    var organs = {
        Head:["headache","sleepy","unresponsiveness","feeling suicidal","mood depressed","unable to concentrate","dizziness","nausea"],
        Chest:["pain chest","shortness of breath","yellow sputum","chest tightness","cough","bradycardia"],
        Upper_abdomen:["distended abdomen","shortness of breath","food intolerance","aphagia"],
        abdomen:["pain abdominal","food intolerance","aphagia","vomiting","hematocrit decreased"],
        Lower_abdomen:["Murphy's sign","diarrhea","constipation","oliguria","urgency of micturition","prostatism"],
        Sexual_organs:["chill","bleeding of vagina","decreased stool caliber","urge incontinence","difficulty passing urine"],
        Eye:["agitation","burning sensation","unconscious state","unsteady gait"],
        Foot_L:["pain foot"],
        Foot_R:["pain foot"],
        Lower_leg_L:["heavy legs","hemiplegia"],
        Lower_leg_R:["heavy legs","hemiplegia"],
        Neck:["neck stiffness","pain neck"],
        Nose:["stuffy nose"],
        Thigh_L:["hemiplegia"],
        Thigh_R:["hemiplegia"],
        Hand_L:["numbness of hand"],
        Hand_R:["numbness of hand"],
        Knee_L:["Knee pain","Knee swelling","Knee pain while moving","feeling of warmth in the joint","stiffness in the knee"],
        Knee_R:["Knee pain","Knee swelling","Knee pain while moving","feeling of warmth in the joint","stiffness in the knee"]
    };
    $('area').on('click',function(){
        var organ = $(this).attr("alt");
        $('#organDropdown').html("<div class='organ-title'>"+organ+"<i class='fa fa-close closeOrgan'></i></div>");
        if(typeof(organs[organ]) != "undefined"){
            var i;
            for (i = 0; i < organs[organ].length; i++) {
                $('#organDropdown').append("<div class='dropdown-item'><p>"+organs[organ][i]+"</p><div class='addBtn'>ADD</div></div>");
            }
        }else{
            $('#organDropdown').append("<div class='dropdown-item'><p>We are sorry we'll cover that organ soon!</p></div>");
        }
        $('#organDropdown').fadeIn();
    });



    $('.iamDisease').on('click',function(){
        $(this).parent().find(".diseses-data").css('right','0px');
        $("html, body").animate({ scrollTop: 0 }, "slow");
    });

    $('.addDisSym').on('click',function(){
        $('#addDis-submit').before('<input type="text" name="dSym[]" placeholder="Enter Symptom" class="form-control">');
    });

    // Form Validation
    $('input[name=dName], textarea[name=dDefinition],input[name=tips], input[name=dSym\\[\\]]').on('blur',function() {
        if($(this).val().length == 0){
            $('.alertMSG').show(500);
            $('#addDis-submit').attr("disabled","disabled");
        }
        else{
            $('.alertMSG').hide(500);
            $('#addDis-submit').removeAttr("disabled");
        }
    });

    $('select').on('blur',function() {
        if($(this).find('option:selected').val().length == 0){
            $('.alertMSG').show(500);
            $('#addDis-submit').attr("disabled","disabled");
        }
        else{
            $('.alertMSG').hide(500);
            $('#addDis-submit').removeAttr("disabled");
        }
    });

    var i = 0;
    $(window).scroll(function() {

        if ($(this).scrollTop() < i) {
          i = $(this).scrollTop();
          $('.navbar').css("top", "0");
        }
        else if ($(this).scrollTop() > 150) {
          i = $(this).scrollTop();
          $('.navbar').css("top", "-80px");
        }
      });

});

  