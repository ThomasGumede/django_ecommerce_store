var csrftoken = Cookies.get("csrftoken");
console.log(csrftoken);
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    }
  },
});

$(document).ready(function () {
  

  $("#follow-btn").on("click", function (e) {
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "/feedback/follow/",
      data: {
        id: $(this).data("id"),
        username: $(this).data("username"),
        action: $(this).data("action"),
      },
      dataType: "json",

      success: function (data) {
        if (data.success) {
          var $prev_action = $("#follow-btn").data("action");
          var $prev_followers = parseInt($("span#followers_count").text());
          $("#follow-btn").data(
            "action",
            $prev_action == "follow" ? "unfollow" : "follow"
          );
          $("#follow-btn").text(
            $prev_action == "follow" ? "Unfollow" : "Follow"
          );

          $("span#followers_count").text(
            $prev_action == "follow" ? $prev_followers + 1 : $prev_followers - 1
          );
        } else {
        }
      },
    });
  });
});
