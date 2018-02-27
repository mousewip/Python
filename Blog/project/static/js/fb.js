// function doLoginAPI(torken) {
//     // console.log(torken);
//     FB.api('/me?fields=id,name,email', function (response) {
//         // check id fb exists
//         $.ajax({
//             url: '/account/checkfid',
//             type: 'POST',
//             data: {'f_': response.id, 'e_': response.email},
//             success: function (dataRSCheck) {
//                 var data = JSON.parse(dataRSCheck);
//                 if (data.code === 200) {
//                     // if id doesn't exists, do register account
//                     // replace email = id fb
//                     $.ajax({
//                         url: '/registerfb',
//                         type: 'post',
//                         data: {
//                             'u_': response.name,
//                             'e_': response.email,
//                             't_': torken,
//                             'f_': response.id
//                         },
//                         success: function (dataRS) {
//                             var data = JSON.parse(dataRS);
//                             if (data.code === 201) {
//                                 $('.spinner').hide();
//                                 show_stack_bar_top('error', 'Oh no!', data.message);
//                             }
//                             else {
//                                 ajaxLoginFB(response.email, torken, response.id);
//                             }
//                         }
//                     });
//                 }
//                 else if (data.code === 201) {
//                     ajaxLoginFB(response.email, torken, response.id);
//                 }
//                 else {
//                     $('.spinner').hide();
//                     show_stack_bar_top('error', 'Oh no!', data.message);
//                 }
//             }
//         });
//     });
// }
//
// function ajaxLoginFB(email, torken, id) {
//     $.ajax({
//         url: '/loginfb',
//         type: 'post',
//         data: {'e_': email, 't_': torken, 'f_': id},
//         success: function (response) {
//             var data = JSON.parse(response);
//             if (data.code === 200)
//                 location.href = "/";
//             else {
//                 $('.spinner').hide();
//                 show_stack_bar_top('error', 'Oh no!', data.message);
//             }
//         }
//     });
// }
//
// function logoutFB() {
//     FB.logout(function (response) {
//         // Person is now logged out
//     });
// }
//
// function checkLoginFB() {
//     FB.getLoginStatus(function (response) {
//         $('.spinner').show();
//         if (response.status === 'connected') {
//             // console.log(response);
//             doLoginAPI(response.authResponse.accessToken);
//         }
//         else {
//             FB.login(function (response) {
//                 // handle the response
//             }, {scope: 'public_profile,email,user_about_me'});
//             $('.spinner').hide();
//         }
//     });
//
// }
//
// window.fbAsyncInit = function () {
//     FB.init({
//         appId: '156445348396184',
//         cookie: true,  // enable cookies to allow the server to access
//                        // the session
//         xfbml: true,  // parse social plugins on this page
//         version: 'v2.12' // use graph api version 2.12
//     });
//
// };
//
// // Load the SDK asynchronously
// (function (d, s, id) {
//     var js, fjs = d.getElementsByTagName(s)[0];
//     if (d.getElementById(id)) return;
//     js = d.createElement(s);
//     js.id = id;
//     js.src = "https://connect.facebook.net/vi_VI/sdk.js";
//     fjs.parentNode.insertBefore(js, fjs);
// }(document, 'script', 'facebook-jssdk'));